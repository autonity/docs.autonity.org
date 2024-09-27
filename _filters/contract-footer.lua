--[[
  This script adds footer navigation buttons to the bottom of the page.
  it is called with:
  ::: {.footer-navigation ....} 
  :::

  and takes the following attributes:
    - prev-url: the url of the previous page
    - prev-contract: the name of the previous contract
    - next-url: the url of the next page
    - next-contract: the name of the next contract
  if no prev-url or next-url is provided, the corresponding button will not be displayed.

  complete example
  ::: {.footer-navigation prev-url="previous-page.qmd" prev-contract="Previous Contract Name" next-url="next-page.qmd" next-contract="Next Contract Name"}
  :::
]]--

function Div(el)
    if el.classes:includes("footer") then
      
      local prev_url = el.attributes["prev-url"]
      local prev_contract = el.attributes["prev-contract"] or "Previous contract"
      local prev_text = "Previous"
      
      local next_url = el.attributes["next-url"]
      local next_contract = el.attributes["next-contract"] or "Next contract"
      local next_text = "Next"

      local version = el.attributes["version"] or "latest"
      
      local wrapper_html = [[
        <div class="contract-footer">
          <div class="footer-navigation">
            %s
          </div>
          <div class="footer-meta-data">
            %s
          </div>
        </div>
      ]]
      
      local prev_html = '<div class="footer-link hidden-link"></div>'

      if prev_url then
        prev_html = string.format([[
          <div class="footer-link prev-link">
            <a href="%s">
             <img class="footer-link-image" src="/_assets/images/chevron-left.svg" class="img-fluid">
            <div class="footer-link-text">
              <span>%s</span>
              <span class="contract-name">%s</span>
            </div>
            </a>
           </div>
        ]], prev_url, prev_text, prev_contract)
      end

      local next_html = '<div class="footer-link hidden-link"></div>'
      if next_url then
        next_html = string.format([[
          <div class="footer-link next-link">
            <a href="%s">
              <div class="footer-link-text">
                <span>%s</span>
                <span class="contract-name">%s</span>
              </div>
              <img class="footer-link-image" src="/_assets/images/chevron-right.svg" class="img-fluid">
            </a>
          </div>
        ]], next_url, next_text, next_contract)
      end

      local version_html = ""
      if version then
        version_html = string.format([[
          <div class="footer-version">
            <span>%s</span>
          </div>
        ]], version)
      end

      local combined_html = string.format('%s%s', prev_html, next_html)

      if combined_html ~= "" then
        local wrapped_html = string.format(wrapper_html, combined_html, version_html)
        return pandoc.RawBlock('html', wrapped_html)
      end
    end
end
