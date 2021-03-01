
#include "_line.h"



namespace Reducto {

	// FUNCIONES DE PYTHON any, maybe...
	// Deberían ser un gruppo de tokens, pasarlo como *args...
	std::string group(std::string token){
		// Puts the string token as (token).
		return "(" + token + ")";
	}


	std::string any(std::string token){
		return group(token) + "*";
	}


	std::string maybe(std::string token){
		return group(token) + "?";
	}


	std::string group_or(std::string token1, std::string token2){
		return "(" + token1 + "|" + token2 + ")";
	}

	// Keep the reference to patterns to avoid instantiating on each method.
	//const Patterns patterns;

	struct Tokens {
		/* Stores the string representation of the patterns to distinguish
		the contents.
		*/

		// Zero or more white space characters
		const std::string whitespace {R"([ \f\t]*)"};

		// 1 or more white space characters
		const std::string whitespace_1 {R"([ \f\t]+)"};

		// One or more #.
		const std::string comment {R"([#+][^\r\n]*)"};

		const std::string comment_line {maybe(whitespace) + comment};

		// Yet to be explained how it works exactly.
		//std::string blank_line {R"((^(\r\n|\n|\r)$)|(^(\r\n|\n|\r))|^\s*$/gm)"};
		// Python's re works ok with the following.
		// std::string blank_line { maybe(whitespace) + R"(\n)" + maybe(whitespace) };
		// In C++'s regex the check must be made against a whitespace character 
		const std::string blank_line {maybe(whitespace) + R"(^\s*$)" + maybe(whitespace) };

		const std::string word { R"(\w+)"};

		const std::string anychar { R"(.*?)"};

		const std::string def_keyword { "def" };
		const std::string async { "async" };  // For asynchronous functions

		// Matches the name of a function only, as func(.
		const std::string def_name { R"([\w+\(])" };

		// Allows posibly typed def functions (using typing convention).
		const std::string def_end {
			maybe(whitespace) + R"(\))" + maybe(whitespace) + maybe(R"(->)") +
			maybe(whitespace) + maybe(word) + maybe(whitespace) + R"(:)"
		};

		const std::string def_start { 
			maybe(whitespace) + maybe(async) + maybe(whitespace) + 
			def_keyword + whitespace_1 + def_name
		};

		const std::string class_keyword { "class" };

		const std::string class_start { maybe(whitespace) + class_keyword + whitespace_1 + def_name};

		// Raw string
		const std::string raw { "r" };

		// Docstrings related tokens
		//const std::string single_str { R"(''')"};
		//const std::string double_str { R"(""")"};
		const std::string single_str { R"('{3})"};
		const std::string double_str { R"("{3})"};
		const std::string docs_grouped { group_or(single_str, double_str) };
		const std::string docs_grouped_end { group_or(single_str, double_str) + '$' };
		// Docstrings one line, start and end
		const std::string docs_one_line {
			//maybe(raw) + docs_grouped + anychar + docs_grouped 
			//maybe(raw) + docs_grouped + R"([\w\W]*?)" + docs_grouped 
			maybe(raw) + docs_grouped + R"([\w\W]*?)" + docs_grouped_end
		};
		const std::string docs_start {
			maybe(whitespace) + maybe(raw) + docs_grouped
		};
		const std::string docs_end {
			//maybe(anychar) + maybe(whitespace) + docs_grouped + maybe(comment_line)
			//anychar + docs_grouped + maybe(comment_line)
			//R"([\w\W]*?)" + docs_grouped //+ maybe(comment_line)
			R"([\w\W]*?)" + docs_grouped_end //+ maybe(comment_line)
		};

	};

	Tokens toks;

	struct Patterns {
		// Stores the regex patterns to simplify access.

		const std::regex comment_line { toks.comment_line };

		const std::regex blank_line { toks.blank_line };

		// Function start
		const std::regex def_start { toks.def_start };

		// Function end (may be necessary for multiline definitions).
		const std::regex def_end { toks.def_end };

		// class start, to distinguish a function ended
		const std::regex class_start { toks.class_start };  //DONE

		// Docstrings
		const std::regex docstrings_one_line { toks.docs_one_line};// DONE

		const std::regex docstrings_start { toks.docs_start};// DONE

		const std::regex docstrings_end { toks.docs_end};  // DONE

	};

	// Regular expressions to filter each line

	static const std::regex COMMENT_LINE(toks.comment_line, std::regex::optimize);

	static const std::regex BLANK_LINE(toks.blank_line, std::regex::optimize);

	static const std::regex DEF_START(toks.def_start, std::regex::optimize);

	static const std::regex DEF_END(toks.def_end, std::regex::optimize);

	static const std::regex CLASS_START(toks.class_start, std::regex::optimize);

	static const std::regex DOCSTRINGS_ONE_LINE(toks.docs_one_line, std::regex::optimize);

	static const std::regex DOCSTRINGS_START(toks.docs_start, std::regex::optimize);

	static const std::regex DOCSTRINGS_END(toks.docs_end, std::regex::optimize);


	//Patterns patterns;

	Line::Line(const string& l): line(l) {}

	int Line::indentation_level() {
		// Asumes a level of indentation is defined by 4 characters
		std::regex re(R"(^\s+)");   // regex for 1 or more whitespaces
		std::smatch matches;  // Container for matches
		int num_matches;
		int indentation = 4;
		if (std::regex_search(line, matches, re)){
			num_matches = matches.length() / indentation;
		    //std::cout << "length: " << matches.length();
		}
		else {
			num_matches = 0;
		}

		return num_matches;
	}

	bool Line::is_comment() {
		//if (std::regex_search(line, patterns.comment_line))
		if (std::regex_search(line, COMMENT_LINE))
			return true;
		return false;
	}

	bool Line::is_blank_line() {
		//if (std::regex_search(line, patterns.blank_line))
		if (std::regex_search(line, BLANK_LINE))
			return true;
		return false;
	}

	bool Line::is_def_start() {
		//if (std::regex_search(line, patterns.def_start))
		if (std::regex_search(line, DEF_START))
			return true;
		return false;
	}

	bool Line::is_def_end() {
		//if (std::regex_search(line, patterns.def_end))
		if (std::regex_search(line, DEF_END))
			return true;
		return false;
	}

	bool Line::is_class_start() {
		//if (std::regex_search(line, patterns.class_start))
		if (std::regex_search(line, CLASS_START))
			return true;
		return false;
	}

	int Line::length(){
		return line.size();
	}


	bool Line::is_docstring_one_line(){
		//if (std::regex_search(line, docstrings_one_line_out))
		//if (std::regex_search(line, patterns.docstrings_one_line))
		if (std::regex_search(line, DOCSTRINGS_ONE_LINE))
			return true;
		return false;
	}

	bool Line::is_docstring_start(){
		//if (std::regex_search(line, docstrings_start_out))
		//if (std::regex_search(line, patterns.docstrings_start))
		if (std::regex_search(line, DOCSTRINGS_START))
			return true;
		return false;
	}

	bool Line::is_docstring_end(){
		//if (std::regex_search(line, docstrings_end_out))
		//if (std::regex_search(line, patterns.docstrings_end))
		if (std::regex_search(line, DOCSTRINGS_END))
			return true;
		return false;
	}

	ostream& operator << (ostream& os, const Line& l) { return os << l.line; }

	unique_ptr<Line> make_line(string l) {
		return make_unique<Line>(l);
	}

}
