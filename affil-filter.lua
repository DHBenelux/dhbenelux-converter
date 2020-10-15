local affil={}

function RawBlock( element )
  if element.text:sub(1, #'\\affil') == '\\affil' then
    table.insert( affil, 1, element.text )
    return element
  else
    return element
  end
end

function Meta( m )
  m.affil = affil
  return m
end
