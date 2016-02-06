#!/usr/bin/env gt
--[[
  Copyright (C) 2016 Sascha Steinbiss <sascha@steinbiss.name>

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
]]

function usage()
  io.stderr:write("Compares two Barrnap GFF3 files.\n")
  io.stderr:write(string.format("Usage: %s <ref> <new>\n" , arg[0]))
  os.exit(1)
end

if #arg < 2 then
  usage()
end

cmp_visitor = gt.custom_visitor_new()
function cmp_visitor:visit_feature(fn)
  local ovl = self.fi:get_features_for_range(fn:get_seqid(), fn:get_range())
  if ovl then
    local prop = ''
    if #ovl == 1 and ovl[1]:get_range() == fn:get_range() then
      prop = " exact"
    end
    print(tostring(fn) .. " has " .. #ovl .. prop .. " overlap(s)")
    for _,v in ipairs(ovl) do
      print("     " .. tostring(v))
    end
  else
    print(tostring(fn) .. " has no overlaps")
  end
  return 0
end

-- set up streams
cmp_stream = gt.custom_stream_new_unsorted()
function cmp_stream:next_tree()
  local node = self.instream:next_tree()
  if node then
    node:accept(cmp_visitor)
  end
  return node
end

-- index new results

fi = gt.feature_index_memory_new()
fs = gt.feature_stream_new(gt.gff3_in_stream_new_sorted(arg[2]), fi)
local gn = fs:next_tree()
while (gn) do
  gn = fs:next_tree()
end

cmp_stream.instream = gt.gff3_in_stream_new_sorted(arg[1])
cmp_visitor.fi = fi
local gn = cmp_stream:next_tree()
while (gn) do
  gn = cmp_stream:next_tree()
end