--- Auto-numbering for Chinese academic documents.
-- H1 = "第X章", H2 = "X.Y", H3 = "X.Y.Z"
-- Figure captions: "图 X-Y：" prefix
-- All handlers in ONE subfilter so counters track document order.

local chapter = 0
local section = 0
local subsection = 0
local fig_count = 0

function Header(el)
    if el.level == 1 then
        chapter = chapter + 1
        section = 0
        subsection = 0
        fig_count = 0
        table.insert(el.content, 1, pandoc.Space())
        table.insert(el.content, 1, pandoc.Str('第' .. tostring(chapter) .. '章'))
    elseif el.level == 2 then
        section = section + 1
        subsection = 0
        table.insert(el.content, 1, pandoc.Space())
        table.insert(el.content, 1, pandoc.Str(tostring(chapter) .. '.' .. tostring(section)))
    elseif el.level == 3 then
        subsection = subsection + 1
        table.insert(el.content, 1, pandoc.Space())
        table.insert(el.content, 1, pandoc.Str(tostring(chapter) .. '.' .. tostring(section) .. '.' .. tostring(subsection)))
    end
    return el
end

function Figure(el)
    fig_count = fig_count + 1
    local prefix = '图 ' .. tostring(chapter) .. '-' .. tostring(fig_count) .. ' '
    -- pandoc 3.x: caption is a Caption object with .long (list of Blocks)
    if el.caption then
        if el.caption.long then
            for _, block in ipairs(el.caption.long) do
                if block.content then
                    table.insert(block.content, 1, pandoc.Str(prefix))
                    break
                end
            end
        elseif type(el.caption) == 'table' and #el.caption > 0 then
            table.insert(el.caption, 1, pandoc.Str(prefix))
        end
    end
    return el
end

-- fallback: pandoc 2.x where images stay in Para
function Para(el)
    if #el.content == 1 and el.content[1].t == 'Image' then
        fig_count = fig_count + 1
        local prefix = '图 ' .. tostring(chapter) .. '-' .. tostring(fig_count) .. ' '
        local img = el.content[1]
        if img.caption and #img.caption > 0 then
            table.insert(img.caption, 1, pandoc.Str(prefix))
        end
    end
    return el
end

-- IMPORTANT: single subfilter to preserve document-order traversal
return {{Header = Header, Figure = Figure, Para = Para}}
