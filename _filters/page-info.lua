return {
  {
    Str = function(elem)
      if elem.text == "{{pageinfo}}" then
        return pandoc.RawInline('html', '<div class="pageinfo pageinfo-primary">')
      elseif elem.text == "{{/pageinfo}}" then
        return pandoc.RawInline('html', '</div>')
      end
      -- Return nil if no condition is met
      return nil
    end
  }
}
