require 'find'
catalog = ARGV[0]
s = ""
Find.find("Plans/#{catalog}"){|f|
	next if f == "." || f == ".."
	s << lambda{File.open(f,'rb'){|r| return r.read}}.call << "\n" rescue next
}
Dir.mkdir('ModHelper') unless Dir.exist?('ModHelper')
File.open('ModHelper/'+catalog.gsub("/","").gsub("\\","")+'.txt','wb'){|w|w.write(s)}
