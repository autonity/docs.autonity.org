return {
  {
    Str = function(elem)
      if elem.text == "{{final}}" then
        return pandoc.RawInline('html', '<span class="badge bg-primary">Final</span>')
      end
      if elem.text == "{{draft}}" then
        return pandoc.RawInline('html', '<span class="badge bg-secondary">Draft</span>')
      end
      if elem.text == "{{public}}" then
        return pandoc.RawInline('html', '<span class="badge bg-info">Public</span>')
      end
      if elem.text == "{{private}}" then
        return pandoc.RawInline('html', '<span class="badge bg-danger">Private</span>')
      end
    end,
  }
}
