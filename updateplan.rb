#encoding: utf-8
require 'open-uri'
require 'find'

$words = {}

module Timetable

	def self.update_words
		wordsdata = lambda{File.open("Schools/Modules/GlobalWords.cfg","rb"){|f|return f.read}}.call
		wordsdata = wordsdata.split("\n")
		wordsdata.each{|x|
			# Pomiń puste wiersze
			next if x.tr(" \n\r\t","")==""
			# Pomiń komentarze
			next if x.include?("#")
			a = x.split("=")
			$words[a[0]] = a[1]
		}
	end

	def self.download_plan(configfile)
		data = lambda{File.open(configfile,'rb'){|f|return f.read}}.call
		mode = 0
		schoolname,schoolsite,schoolfolder = nil
		schoolmodule = "VULCAN" # Default module to use
		classes = {}
		data.split("\n").each{|x|
			x = x.tr("\t\r\n","")
			next if x == "" || x.gsub(" ","") == ""
			args = x.split("=")
			if mode == 0 # START
				$classes = {}
				case args[0]
				when "MODE"
					case args[1]
					when "START" then mode = 0
					when "CLASSES" then mode = 1
					end
				when "NAME"
					schoolname = args[1]
				when "FOLDER"
					schoolfolder = args[1]
				when "SITE"
					schoolsite = args[1]
				when "MODULE"
					schoolmodule = args[1]
				end
			elsif mode == 1 # CLASSES
				case args[0]
				when "MODE"
					case args[1]
					when "START" then mode = 0
					when "CLASSES" then mode = 1
					end
				else
					if args[0] != nil && args[1] != nil && args[0] != "" && args[1] != ""
						classes[args[0]] = args[1]
					end
				end
			end
		}
		classes.each{|k,v|
			lambda {
				Dir.mkdir(schoolfolder) unless Dir.exist?(schoolfolder)
				open("#{schoolsite}#{v}.html"){|s|
					File.open("#{schoolfolder}#{k}.ncp",'wb'){|w|w.write(Marshal.dump(Timetable.convert_to_table(s.read)))}
					print "#{schoolname} - Plan lekcji dla klasy #{k} pobrany.\n"
					Timetable.convert_table_to_text("#{schoolfolder}#{k}.ncp")
					File.delete("#{schoolfolder}#{k}.ncp")
					print "#{schoolname} - Plan lekcji dla klasy #{k} przekonwertowany.\n"
				}
			}.call rescue lambda { print "#{schoolname} - Błąd przy pobieraniu klasy #{k}\n" }.call
		}
	end
				
	def self.download_latest
		Find.find("Schools/Modules").each{|x|
			next if x.split(".")[-1] != "cfg"
			Timetable.download_plan(x)
		}
	end
	
	def self.remove_tags(x)
		removedtags = x.gsub("<span style=\"font-size:85%\"","").gsub("<span style=\"font-size:80%\"","").gsub("<span class=\"s\"","").gsub("<span class=\"n\"","")
		return removedtags
	end
	
	def self.convert_to_table(html)
		data = html
		#data = lambda{File.open(htmlfile,'rb'){|f| return f.read}}.call
		# $table[[[poniedziałek lekcja 1, poniedziałek lekcja 2, poniedziałek lekcja3],[wtorkowy plan],..[piątkowy plan]]
		$table = [0,[],[],[],[],[]]
		$current_lection_nr = 1 # Aktualny numer lekcji
		$current_day = 1 # Aktualny dzień
		data.split("\n").each{|line|
			# Line that represent lection number
			if line.include?("<td class=\"nr\">")
				# Remove formatting
				fline = line.gsub("\n","").gsub("\r","").gsub("\t","")
				# Get number
				fline = fline.gsub("<td class=\"nr\">","").gsub("</td>", "")
				$current_lection_nr = fline.to_i
			end
			# Line that represent subject to current lection
			if line.include?("<td class=\"l\">")
				# Remove formatting
				fline = line.gsub("\n","").gsub("\r","").gsub("\t","")
				# Remove tags - level 1 (td)
				fline = fline.gsub("<td class=\"l\">","").gsub("</td>", "")
				# Check that lesson is empty
				if fline.include?("&nbsp;")
					$table[$current_day][$current_lection_nr] = ""
					$current_day += 1
					$current_day = 1 if $current_day == 6
				elsif line.include?("<span class=\"p\"")
					# $result = [subject, teacher, classroom]
					$result = ""
					# Lesson is not empty
					# <span class="p">historia</span> <a href="n51.html" class="n">PR</a> <a href="s21.html" class="s">210</a>
					# Parse dla wielu języków
					if fline.include?("<br>")
						fsplit3 = fline.gsub("<br>","<br>$xyz$").split("<br>")
					elsif fline.include?("<br/>")
						fsplit3 =  fline.gsub("<br/>","<br/>$xyz$").split("<br/")
					else
						fsplit3 = [fline]
					end
					fsplit3.each{|fline|
						# Remove tags - level 2 (span)
						fline = fline.gsub("<span class=\"p\">","").gsub("</span>","")
						#historia <a href="n51.html" class="n">PR</a> <a href="s21.html" class="s">210</a>
						fsplit2 = fline.split("<a")
						fsplit = fsplit2.at(0)
						# Remove > sign and space at end
						fsplit = Timetable.remove_tags(fsplit.gsub(">","").gsub("</a",""))
						fsplit[-1] = "" if fsplit[-1] == "\x20"
						# Set subject name
						subject = fsplit.gsub("$xyz$","\n").split("\n").map{|z|z.capitalize}.join("\n")
						$result << "#{subject} "
						# Set teacher name
						lambda{
						fsplit = fsplit2.at(1).split(">")[1]
						fsplit = Timetable.remove_tags(fsplit.gsub("</a","").gsub("\x20",""))
						$result << "#{fsplit} "
						# Set classroom nr
						fsplit = fsplit2.at(2).split(">")[1]
						fsplit = Timetable.remove_tags(fsplit.gsub("</a>","").gsub("\x20","").gsub("Sala_","").gsub("Sala",""))
						fsplit = fsplit.gsub("<a>","").gsub("</a","")
						$result << "#{fsplit}"
						}.call rescue lambda{}.call
					}
					# Save result to main table
					$table[$current_day][$current_lection_nr] = $result
					$current_day += 1
					$current_day = 1 if $current_day == 6
				end
			end
		}
		return $table
	end
	
	def self.convert_table_to_text(tablefile)
		data = Marshal.load(lambda{File.open(tablefile,'rb'){|f| return f.read}}.call)
		$result = ""
		$current_day = 1
		$weekday = 0
		data.each{|x|
			next if x == nil || x == 0
			$weekday += 1
			$weekday = 1 if $weekday == 6
			count = 0
			x.each{|y|
				next if y == nil
				count += 1
				$words.each{|a,b|
					y = y.gsub(a,b) if y.include?(a)
				}
				$result << "#{count}. #{y}\n"
			}
			#$result[-1] = "" if $result[-1] = "\n"
			name = tablefile.gsub('.ncp','')+$weekday.to_s+'.txt'
			File.open(name,'wb'){|w|w.write($result)}
			$result = ""
		}
	end
end

begin
	Timetable.update_words
	Dir.mkdir('Plans') unless Dir.exist?('Plans')
	if ARGV[0] != nil
		Timetable.download_plan("Schools/Modules/#{ARGV[0]}.cfg")
	else
		Timetable.download_latest
	end
end
