#Algoritmo probabilistico, Daniel Correa
=begin
	That is a simple game, you try with a coin, if the diference betwen head and tail is 3 you will win $8, but you lose $1 for any try. do you will play the game?
=end	
def coin(n)
	benefit = 0
	averageBenefit = 0
	for i in 0 .. n
		binary = 0
		head=0
		tail=0
		try=0
		while (head-tail).abs != 3 do 
			binary = Random.rand(1..2)
			#puts binary
			if binary == 1  
				head += 1
			else  
				tail += 1
			end 
			try += 1
		end
		benefit += 8.0 - try
	end 
	averageBenefit = benefit/n
	return averageBenefit
end

puts coin(1000)