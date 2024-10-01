function Div(el)
    -- Check if the div has the class "meta-data"
    local has_meta_data_class = false
    for _, class in ipairs(el.classes) do
        if class == "meta-data" then
            has_meta_data_class = true
            break
        end
    end

    if has_meta_data_class then
        local mutability_type = el.attributes["mutability-type"]
        local selector_type = el.attributes["selector"]

        local color_class = ""
        if mutability_type == "payable" then
            color_class = "payable-tag"
        elseif mutability_type == "view" then
            color_class = "view-tag"
        elseif mutability_type == "pure" then
            color_class = "pure-tag"
        end

        local wrapper_html = [[
            <div class="method-meta-data-wrapper">
            %s
            </div>
        ]]
        
        local tag_html = ""
        if color_class ~= "" then
            tag_html = string.format([[
                <div class="mutability-wrapper"><span class="mutability-tag %s">%s</span></div>
            ]], color_class, mutability_type)
        end

        local selector_html = ""
        if selector_type then
            selector_html = string.format([[
                <div class="selector-wrapper"><span class="selector">%s</span></div>
            ]], selector_type)
        end

        local combined_html = string.format('%s%s', tag_html, selector_html)

        if combined_html ~= "" then
            local wrapped_html = string.format(wrapper_html, combined_html)
            return pandoc.RawBlock('html', wrapped_html)
        end
    end
end
