#ifndef pyfile_h
#define pyfile_h

#include <iostream>
#include <fstream>
#include <sstream>
#include <iterator>
#include <string>
#include <regex>
#include <vector>
#include <algorithm> 
#include "_line.h"
//#include "function.h"


namespace Reducto {


	struct FileStats {
		// Stores the results of a processed file.
		int number_of_lines;  // Number of lines in the file.
		int max_line_length;  // Max number of characters of the longest line.
		int docstrings;  // Number of lines which are docstrings.
		int comment_lines;  // 
		int blank_lines;
		std::vector<int> functions;
	};


	class PyFile {
		public:
			// Default constructor
			PyFile();

			// Constructor from the filename
			PyFile(const std::string& f);

			// Read the file and store it in content
			void grab_info();

			// NEW METHOD. USES LINES INSTEAD OF UNIQUE_PTR TO LINE
			// DOESN'T CONSTRUCT FUNCTIONS.
			void collect();
			//void grab_info_no_function();

			// Count the number of functions in a processed src file.
			int number_of_functions();

			int number_of_lines();

			int number_of_comment_lines();

			int number_of_blank_lines();

			int number_of_docstring_lines();

			int get_max_line_length();

			void get_functions();

			void grab_functions_info();

			void print_functions_info();

			FileStats stats();

			//std::vector<Reducto::FunctionStats> get_function_stats();

		    std::string get_filename() { return filename; }

		private:
			// Store the filename
			std::string filename;

  			// Stores the functions detected in the file.
  			//std::vector<Reducto::Function> functions;

  			// Counter to keep track of items. Maybe redirected to a container?
  			int num_lines = 0;
  			int comment_lines = 0;
  			int docstring_lines = 0;
  			int blank_lines = 0;
  			int max_line_length = 0;
  			std::vector<int> function_sizes;
			// To avoid calling collect more than once, otherwise values maybe overwritten.
			bool _collected = false;

			FileStats get_stats();

  			// To keep track of whether the Function's method grab_info was called
  			//bool _functions_grabbed = false;

	};

}


#endif