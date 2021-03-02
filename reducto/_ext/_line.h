#ifndef LINE_H
#define LINE_H

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <regex>
#include <memory>

using namespace std;


namespace Reducto {

	// Functions to deal with regex formation.
	std::string group(std::string token);

	std::string any(std::string token);

	std::string maybe(std::string token);

	std::string group_or(std::string token1, std::string token2);


	class Line {

		public:
			// Constructor with string.
			//Line(string l);
			Line(const string& l);

			// Default destructor
			~Line() = default;

			string get_line() { return line; }

			// Gets the indentation level of the line.
			int indentation_level();

			// Checks wheter a line is a comment or not (looking for #).
			bool is_comment();

			// Checks whether a line contains only a \n.
			bool is_blank_line();

			// Counts the number of chars in a string, to get the max line length.
			int length();

			bool is_def_start();

			bool is_def_end();

			bool is_class_start();

			bool is_docstring_one_line();

			bool is_docstring_start();

			bool is_docstring_end();

			friend ostream& operator<<(ostream& os, const Line& l);

		private:
			string line;

	};

	unique_ptr<Line> make_line(string l);

}


#endif
