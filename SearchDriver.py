from Searches import Searches


write_file = "Files/search_results.txt"
open(write_file, 'w').close()
with open(write_file, 'a') as file:
    for i in range(8):
        file.write("Trial {}".format(i+1))
        file.write("\n\nGreedy Search: ")
        file.write("\n" + Searches.greedy_search("Files/adPlac1.csv", 100))
        file.write("\n" + Searches.greedy_search("Files/adPlac2.csv", 5000))
        file.write("\n\nGenetic Algorithm: ")
        file.write("\n" + Searches.genetic_search("Files/adPlac1.csv", 100, 7))
        file.write("\n" + Searches.genetic_search("Files/adPlac2.csv", 5000, 6) + "\n\n")
