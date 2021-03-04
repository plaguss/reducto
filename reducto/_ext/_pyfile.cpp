
#include "_pyfile.h"


namespace Reducto {


	// Constructors
	PyFile::PyFile() {}

	PyFile::PyFile(const std::string& f) { filename = f; }

	//void PyFile::grab_info_no_function() {
	void PyFile::collect() {

		if (_collected)  // Avoid recollecting data.
			return;

	    std::ifstream file(filename);
	    std::string line; 

  		// To keep control of whether we are constructing a function or docstring
  	    bool in_function = false;
  	    bool in_docstring = false;

  	    // Variable to control the indententation level of the function if started.
  	    // Starts at 0 (the first function is expected to start at the first level...)
  	    int function_started = 0;

  	    // PROBAR PARA CONTAR LINEAS DE FUNCIONES SIN CREAR OBJETO
  	    int source_lines = 0;  // DEBE INICIALIZARSE EN CADA NUEVA FUNCIÓN PARA CONTAR BIEN.

  	    // IT IS NOW A PRIVATE VARIABLE
  	    //std::vector<int> function_sizes;

  	    int i = 0;
  	    std::cout << "START TO GRAB INFO " << '\n';

		while (std::getline(file, line)) {

			i++;
			num_lines++;

			int line_length = line.length();
			max_line_length = std::max(max_line_length, line_length);

			auto content = Reducto::Line(line);

			int level = content.indentation_level();

			//std::cout << i <<"LINE " << line << '\n';

			if (in_function) {  // Inside of a function.
				// TODO: export to a separate function
				if (level > function_started) {  // Indented, maybe source or docstring
					// INTENTAR COMPROBAR IN DOCSTRING ANTES!
					if (in_docstring) {
						docstring_lines++;
						if (content.is_docstring_end())
							in_docstring = false;
					}
					else if (content.is_docstring_start()) {
						docstring_lines++;
						in_docstring = true;
						if (content.is_docstring_end()) {
							in_docstring = false;
						}
					}
					else {
						if (content.is_blank_line())
							blank_lines++;
						else if (content.is_comment())
							comment_lines++;
						else {
							// Line of code of a function
							source_lines++;
						}
					}
					continue;
				}
				else {  // TODO: ESTO TIENE QUE IR DENTRO DE Function, o un solo check?
					if (content.is_blank_line()) {
						blank_lines++;
					}
					else if (content.is_comment()) {
						comment_lines++;
					}
					else if (content.is_def_start()) {
						//std::cout << i << " - def inside -" << line << '\n';
						function_sizes.push_back(source_lines);
						in_function = true;  // Start function loop.
						source_lines = 1;  // Restart source lines for a new function.
					}
					else if (content.is_class_start()) {
						// Finishes a function 
						function_sizes.push_back(source_lines);
						source_lines = 0;  // Restart source lines.
						in_function = false;
					}
					else if (content.is_def_end()) {
						//std::cout << i << " --> else -" << line << '\n';
						source_lines++;
					}
					else {
						in_function = false;
						source_lines++;
						std::cout << i << " WEIRd -" << line << '\n';
						// if __name__ == __main__ goes here (Scripts?)
						// WHAT IS THIS?
					}
					continue;  // We are no longer in a function
				}
			}
			else if (in_docstring) {  // CHECKEAR QUE EXISTE CONTENT!

				docstring_lines++;

				if (content.is_docstring_end()) {
					in_docstring = false;
				}
				continue;
			}
			else {
				if (content.is_blank_line())
					blank_lines++;
				else if (content.is_comment())
					comment_lines++;
			}

			if (content.is_def_start()) {
				// Only push back functions after the first.
				std::cout << i << " = def start = " << line << '\n';
				if (source_lines > 0) {
					// In case a previous function existed on the loop.
					function_sizes.push_back(source_lines);
					source_lines = 0;
				}
				source_lines++;
				// Start the counter for a new function.
				function_started = level;
				in_function = true;
			}
			// Check both cases, to catch docstrings inside a function,
			// from inside function calls.
			else if (content.is_docstring_start()) {
				docstring_lines++;
				in_docstring = true;

				if (content.is_docstring_end())
					in_docstring = false;
			}
		}
		// Insert the last function which didn't trigger the end.
		if (in_function)
			function_sizes.push_back(source_lines);
		// LO SIGUIENTE SOLO PARA PROBAR
		std::cout << "docstrings: " << docstring_lines << '\n';
		std::cout << "comments: " << comment_lines << '\n';
		std::cout << "blank_lines: " << blank_lines << '\n';
		std::cout << "functions: " << function_sizes.size() << '\n';
		int j = 0;
		for (auto sz: function_sizes) {
			j++;
			std::cout << j << " - source lines: " << sz << '\n';
		}
		_collected = true;
	}

	// Process file line by line
	/*
	void PyFile::grab_info() {

	    std::ifstream file(filename);
	    std::string line; 

  		// To keep control of whether we are constructing a function or docstring
  	    bool in_function = false;
  	    bool in_docstring = false;

  	    // Variable to control the indententation level of the function if started.
  	    // Starts at 0 (the first function is expected to start at the first level...)
  	    int function_started = 0;

  	    // PROBAR PARA CONTAR LINEAS DE FUNCIONES SIN CREAR OBJETO
  	    int function_lines = 0;
  	    std::vector<int> function_sizes;


  	    // FIXME, this function is created just to avoid a non-declared error.
  	    Reducto::Function current_function; 

  	    int i = 0;

		while (std::getline(file, line)) {
			i++;
			num_lines++;

			int line_length = line.length();
			max_line_length = std::max(max_line_length, line_length);

			auto content = Reducto::make_line(line);
			//auto content = Reducto::Line(line);

			//int level = content.indentation_level();
			int level = content->indentation_level();

			if (in_function) {  // Inside of a function.
				// TODO: export to a separate function
				if (level > function_started) {
					//continue;
					//current_function.add_line(content);
					current_function.add_line(std::move(content));

					// AQUÍ HABRÍA QUE PROBAR DE NUEVO CADA CASO PARA
					//std::cout << "level > funcstarted " << line << '\n';

				}
				else {  // TODO: ESTO TIENE QUE IR DENTRO DE Function, o un solo check?
					//if (content.is_blank_line() || content.is_class_start()) {
					if (content->is_def_start() || content->is_class_start()) {
						std::cout << i << ", --line " << line << '\n';

						in_function = false;
						//functions.push_back(current_function);
						functions.push_back(std::move(current_function));
						//continue;
					}

					//else if (content.is_def_start() || content.is_class_start()) {
					else if (content->is_blank_line() || content->is_comment() || content->is_def_end()) {
						//current_function.add_line(content);
						current_function.add_line(std::move(content));
					}
					// We are no longer in a function
				}
			}
			else if (in_docstring) {  // CHECKEAR QUE EXISTE CONTENT!

				docstring_lines++;

				//if (content.is_docstring_end()) {
				if (content->is_docstring_end()) {
					in_docstring = false;
					continue;
				}
			}
			else {
				//if (content.is_blank_line()) {
				if (content->is_blank_line()) {
					blank_lines++;
				}
				//else if (content.is_comment()) {
				else if (content->is_comment()) {
					comment_lines++;
				}
			}

			// Check whether the line has been moved.
			// Otherwise, a runtime error would appear
			if (content) {
				if (content->is_def_start()) {
			//if (content.is_def_start()) {

					if (current_function.size() > 0) {
						//functions.push_back(current_function);
						functions.emplace_back(std::move(current_function));

						// >> NEW
						function_sizes.push_back(function_lines);
					}
					// >> NEW
					function_lines++;

					//Reducto::Function current_function(content);
					Reducto::Function current_function(std::move(content));

					function_started = level;
					in_function = true;
				}
				// Check both cases, to catch docstrings inside a function,
				// from inside function calls.
				else if (content->is_docstring_start() && !in_function) {
				//else if (content.is_docstring_start() && !in_function) {

					docstring_lines++;

					if (!content->is_docstring_one_line())
					//if (!content.is_docstring_one_line())
						in_docstring = true;
				}
			}
		}
	}

	int PyFile::number_of_functions() {
		return functions.size();
	}
	*/

	int PyFile::number_of_lines() {
		return num_lines;
	}

	int PyFile::number_of_comment_lines() {
		return comment_lines;
	}

	int PyFile::number_of_blank_lines() {
		return blank_lines;
	}

	int PyFile::number_of_docstring_lines() {
		return docstring_lines;
	}

	int PyFile::get_max_line_length() {
		return max_line_length;
	}

	FileStats PyFile::get_stats() {

		FileStats _stats;

		_stats.number_of_lines = num_lines;
		_stats.max_line_length = max_line_length;
		_stats.docstrings = docstring_lines;
		_stats.comment_lines = comment_lines;
		_stats.blank_lines = blank_lines;
		_stats.functions = function_sizes;

		return _stats;

	}

	FileStats PyFile::stats() {

		if (!_collected)
			collect();

		return get_stats();

	}

	/*
	void PyFile::grab_functions_info() {
		if (!_functions_grabbed) {
			for (auto&& f: functions)
				f.grab_info();

			_functions_grabbed = true;

		}
	}

	void PyFile::print_functions_info() {
		//for (auto&& f: functions)
		for (auto&& f: functions)
			f.print_info();
	}

	std::vector<Reducto::FunctionStats> PyFile::get_function_stats() {

		// First call grab_functions_info if the method wasn't called.
		if (!_functions_grabbed) {
			grab_functions_info();
			_functions_grabbed = true;  // Set the value to false to avoid recomputing.
		}

		std::vector<Reducto::FunctionStats> _stats;

		for (auto&& f: functions)
			_stats.push_back(f.stats());

		return _stats;
	}
	*/
}

