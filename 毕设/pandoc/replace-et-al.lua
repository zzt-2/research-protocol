-- replace-et-al.lua
-- Pandoc Lua filter: replace "et al." with "等" only for entries with Chinese author names
-- Avoids false triggers from CSL-generated Chinese (e.g. "卷", "版")
function Para(el)
  local text = pandoc.utils.stringify(el)
  -- Only match if the first 80 chars (author area) contain CJK
  local header = text:sub(1, 80)
  if header:match("[\228-\233][\128-\191][\128-\191]") then
    local new_text = text:gsub("et al%.", "等")
    if new_text ~= text then
      return pandoc.Para(pandoc.Str(new_text))
    end
  end
  return el
end
