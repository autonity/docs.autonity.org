---
title: "Oracle Contract Interface"
linkTitle: "Oracle Contract Interface"

description: >
  Autonity Oracle Contract functions
---

Interface for interacting with Autonity Oracle Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.
- JSON-RPC methods to submit calls to inspect state.

{{% pageinfo %}}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction from Autonity Utility Tool (aut)](/account-holders/submit-trans-aut/).
{{% /pageinfo %}}

## getPrecision

/**
    * @notice Precision to be used with price reports
    */
    function getPrecision() external pure returns (uint256) {
        return PRECISION;
    }
## getVotePeriod
    /**
    * @notice vote period to be used for price voting and aggregation
    */
    function getVotePeriod() external view returns (uint) {
        return votePeriod;
    }


## vote

modifier:     modifier onlyVoters {
        require(votingInfo[msg.sender].isVoter, "restricted to only voters");
        _;
    }

/**
    * @notice Vote for the current period. In order to save gas,
    * if (reports[i] == INVALID_PRICE)g the symbols.
    * if the validator leave consensus committee then his vote is discarded.
    * if a validator joins the consensus committee then his first vote is not
    * taken into account.
    * Only allowed to vote once per round.
    * @param _commit hash of the new reports
    *        _reports reveal of the reports for the previous cycle.
    *        _salt  slat value which was used to generate last round commitment
    */
    function vote(uint256 _commit, int256[] calldata _reports, uint256 _salt) onlyVoters external {
        //revert if already voted for this round
        // voters should not be allowed to vote multiple times in a round
        // because we are refunding the tx fee and this opens up the possibility
        // to spam the node
        require(votingInfo[msg.sender].round != round, "already voted");

        uint256 _pastCommit = votingInfo[msg.sender].commit;
        // Store the new commit before checking against reveal to ensure an updated commit is
        // available for the next round in case of failures.
        votingInfo[msg.sender].commit = _commit;
        uint256 _lastVotedRound  = votingInfo[msg.sender].round;
        // considered to be voted whether vote is valid or not
        votingInfo[msg.sender].round = round;
        // new voter/first round
        if (_lastVotedRound == 0 ) {
            return;
        }

        // if data is not supplied and voter is not a new voter
        // report must contain the correct price
        if(_reports.length != symbols.length)  {
            return;
        }

        if ( _lastVotedRound != round -1 ||
            _pastCommit != uint256(keccak256(abi.encodePacked(_reports, _salt, msg.sender)))) {
            // If missed a round OR reveal does not matches past commit
            // fill invalid_price in the reports for these voters
            for (uint256 i = 0; i < symbols.length; i++) {
                reports[symbols[i]][msg.sender] = INVALID_PRICE;
            }
            // we return the tx fee in all cases, because in both cases voter is slashed during aggregation
            // phase, because the reports contain invalid prices
            return;
        }
        // Voter has to vote on all the symbols
        // uint256 MAX_INT = uint256(-1) is a special value
        for (uint256 i = 0; i < _reports.length; i++) {
             reports[symbols[i]][msg.sender] = _reports[i];
        }
    }

## finalize
 /**
     * @notice Called once per VotePeriod part of the state finalisation function.
     *
     */
    function finalize() onlyAutonity public {
        if (block.number >= lastRoundBlock + votePeriod){
            for(uint i = 0; i < symbols.length; i += 1 ) {
                aggregateSymbol(i);
            }

            // this votingInfo is updated with the newVoter set just so that the new voters
            // are able to send their first vote, but they will not be used for aggregation
            // in this round
            if (lastVoterUpdateRound == int256(round)) {
                for(uint i = 0; i < newVoters.length; i++) {
                    votingInfo[newVoters[i]].isVoter = true;
                }
            }
            //votingInfo update happens a round later then setting of new voters,
            // because we still want to aggregate vote for lastVoterSet in the voterupdateround+1
            if (lastVoterUpdateRound+1 == int256(round)) {
                _updateVotingInfo();
            }
            lastRoundBlock = block.number;
            round += 1;
            // symbol update should happen in the symbolUpdatedRound+2 since we expect
            // oracles to send commit for newSymbols in symbolUpdatedRound+1 and reports
            // for the new symbols in symbolUpdatedRound+2
            if (int256(round) == symbolUpdatedRound+2) {
                symbols = newSymbols;
            }
            emit NewRound(round, block.number, block.timestamp, votePeriod);
        }
    }
## aggregateSymbol

/**
     * @notice Level 2 aggregation routine. The final price
     * is the median of all price collected.
     * @dev This method is responsible for detecting and calling the appropriate
     * accountability functions in case of missing or malicious votes.
     */
    function aggregateSymbol(uint _sindex) internal {
        string memory _symbol = symbols[_sindex];
        // Final aggregation doesn't depend on price.
        int256[] memory _totalReports = new int256[](voters.length);
        uint256 _count;
        for(uint i = 0; i < voters.length; i++) {
            address  _voter = voters[i];
            // if voter has missed this round OR INVALID price reveal was submitted
            if(votingInfo[_voter].round != round || reports[_symbol][_voter] == INVALID_PRICE) {
                // TODO: Implement Slashing
                //autonity.oracleVoteMissing(voters[i]);
                continue;
            }
            _totalReports[_count++] = reports[_symbol][_voter];
        }
        int256 _priceMedian = prices[round-1][_symbol].price;
        PriceStatus pStatus = PriceStatus.FAILURE;
        if (_count > 0) {
            _priceMedian = _getMedian(_totalReports, _count);
            pStatus = PriceStatus.SUCCESS;
        }
        prices.push();
        prices[round][_symbol] = Price(
            _priceMedian,
            block.timestamp,
            pStatus);

    }

## latestRoundData

/**
     * @notice Return latest available price data.
     * @param _symbol, the symbol from which the current price should be returned.
     */
    function latestRoundData(string memory _symbol) public view returns (RoundData memory data) {
        //return last aggregated round
        Price memory _p = prices[round-1][_symbol];
        RoundData memory _d = RoundData(round-1, _p.price, _p.timestamp, uint(_p.status));
        return _d;
    }

## getRoundData

 /**
     * @notice Return price data for a specific round.
     * @param _round, the round for which the price should be returned.
     * @param _symbol, the symbol for which the current price should be returned.
     */
    function getRoundData(uint256 _round, string memory _symbol) external view returns
    (RoundData memory data) {
        Price memory _p = prices[_round][_symbol];
        RoundData memory _d = RoundData(_round, _p.price, _p.timestamp, uint(_p.status));
        return _d;
    }


## setSymbols
   // ["NTNUSD", "NTNEUR", ... ]
    function setSymbols(string[] memory _symbols) external onlyOperator {
        require(_symbols.length != 0, "symbols can't be empty");
        require((symbolUpdatedRound+1 != int256(round)) && (symbolUpdatedRound != int256(round)), "can't be updated in this round");
        newSymbols = _symbols;
        symbolUpdatedRound = int256(round);
        // these symbols will be effective for oracles from next round
        emit NewSymbols(_symbols, round+1);
    }
## getSymbols
    function getSymbols() external view returns(string[] memory) {
        // if current round is the next round of the symbol update round
        // we should return the updated symbols, because oracle clients are supposed
        // to use updated symbols to fetch data
        if (symbolUpdatedRound+1 == int256(round)) {
            return newSymbols;
        }
        return symbols;
    }
## getVoters

  function getVoters() external view returns(address[] memory) {
        return newVoters;
    }
## getRound

    function getRound() external view returns (uint256) {
        return round;
    }


## _updateVotingInfo

  function _updateVotingInfo() internal {
        uint _i = 0;
        uint _j = 0;

        while ( _i < voters.length && _j < newVoters.length){
            if(voters[_i] == newVoters[_j]){
                _i++;
                _j++;
                continue;
            } else if(voters[_i] < newVoters[_j]){
                // delete from votingInfo since this voter is not present in the new Voters
                delete votingInfo[voters[_i]];
                _i++;
            } else {
                _j++;
            }
        }

        while ( _i < voters.length) {
            // delete from voted since it's not present in the new Voters
            delete votingInfo[voters[_i]];
            _i++;
        }
        voters = newVoters;
    }

## setVoters

    function setVoters(address[] memory _newVoters) onlyAutonity public {
        require(_newVoters.length != 0, "Voters can't be empty");
        _votersSort(_newVoters, int(0), int(_newVoters.length - 1));
        newVoters = _newVoters;
        lastVoterUpdateRound = int256(round);
    }

## _votersSort

   /**
    * @dev QuickSort algorithm sorting addresses in lexicographic order.
    */
    function _votersSort(address[] memory _voters, int _low, int _high)
    internal pure {
        int _i = _low;
        int _j = _high;
        if (_i == _j) return;
        address _pivot = _voters[uint(_low + (_high - _low) / 2)];
        // Set the pivot element in its right sorted index in the array
        while (_i <= _j) {
            while (_voters[uint(_i)] > _pivot) _i++;
            while (_pivot > _voters[uint(_j)]) _j--;
            if (_i <= _j) {
                (_voters[uint(_i)], _voters[uint(_j)]) =
                (_voters[uint(_j)], _voters[uint(_i)]);
                _i++;
                _j--;
            }
        }
        // Recursion call in the left partition of the array
        if (_low < _j) {
            _votersSort(_voters, _low, _j);
        }
        // Recursion call in the right partition
        if (_i < _high) {
            _votersSort(_voters, _i, _high);
        }
    }

## _getMedian

   /**
    * @dev QuickSort algorithm sorting addresses in lexicographic order.
    */
    function _getMedian(int256[] memory _priceArray, uint _length) internal pure returns (int256) {
        if (_length == 0) {
            return 0;
        }
        _sortPrice(_priceArray, 0, int(_length -1));
        uint _midIndex = _length/2;
        return (_length % 2 == 0) ? (_priceArray[_midIndex-1] + _priceArray[_midIndex])/2 : _priceArray[_midIndex];
    }

## _sortPrice


    function _sortPrice( int256[] memory _priceArray, int _low, int _high) internal pure {
        int _i = _low;
        int _j = _high;
        if (_i == _j)  return;
        int256 pivot = _priceArray[uint(_low+(_high-_low)/2)];
        while (_i <= _j) {
            while(_priceArray[uint(_i)] < pivot) _i++;
            while(pivot < _priceArray[uint(_j)]) _j--;
            if (_i <= _j) {
                (_priceArray[uint(_i)], _priceArray[uint(_j)]) = (_priceArray[uint(_j)], _priceArray[uint(_i)]);
                _j--;
                _i++;
            }
        }
        // recurse left partition
        if (_low < _j) {
            _sortPrice(_priceArray, _low, _j);
        }
        // recurse right partition
        if (_i < _high ) {
            _sortPrice(_priceArray, _i, _high);
        }
        return ;
    }




