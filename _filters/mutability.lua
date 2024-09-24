function Div(el)
    if el.classes:includes("mutability") then
        local mutability_type = el.attributes["mutability-type"]

        local color_class = ""
        if mutability_type == "payable" then
            color_class = "payable-tag"
        elseif mutability_type == "view" then
            color_class = "view-tag"
        elseif mutability_type == "pure" then
            color_class = "pure-tag"
        end

        local tag_html = ""
        if color_class ~= "" then
            tag_html = string.format([[
                <div class="mutability-wrapper"><span class="mutability-tag %s">%s</span></div>
            ]], color_class, mutability_type)
        end

        if tag_html ~= "" then
            return pandoc.RawBlock('html', tag_html)
        end
    end
end
