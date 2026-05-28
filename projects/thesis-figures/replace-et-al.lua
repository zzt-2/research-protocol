-- replace-et-al.lua
-- Pandoc Lua filter: replace "et al." with "等" in bibliography entries containing Chinese
function Para(el)
  local text = pandoc.utils.stringify(el)
  if text:match("[\228-\233][\128-\191][\128-\191]") then
    local new_text = text:gsub("et al%.", "等")
    if new_text ~= text then
      return pandoc.Para(pandoc.Str(new_text))
    end
  end
  return el
end
