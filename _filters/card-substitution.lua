return {
  {
    Str = function(elem)
      if elem.text == "{{card}}" then
        return pandoc.RawInline('html', '<div class="card">')
      elseif elem.text == "{{/card}}" then
        return pandoc.RawInline('html', '</div>')
      end
      -- Return nil if no condition is met
      return nil
    end
  }
}
