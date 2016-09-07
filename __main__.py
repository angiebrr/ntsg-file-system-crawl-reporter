from arguments import Arguments
from datetime import datetime
from sqlite_reporter import SqliteReporter
import logging

def main():
    """The main method of the file crawl reporter program

        This will:
        - Parse arguments (see arguments.py)
        - Create a SqlReporter that will either generate csv reports for all crawls in general or for all users
        - Log errors that occurred while reporting
    """

    # Parse and collect all arguments
    scriptArgs = Arguments()

    # Create logger; put it in the same path as the output
    loggerPath = filename=scriptArgs.outputPath + '/report_script.log'
    with open(loggerPath, 'w') as file: pass
    logging.basicConfig(filename=scriptArgs.outputPath + '/report_script.log', level=logging.DEBUG)
    logging.info("[{timestamp}]: Generating reports from sqlite file {input}, and output directory {output} \r".format
    (
        timestamp=str(datetime.now()),
        input=scriptArgs.inputFile,
        output=scriptArgs.outputPath
    ))

    # Create the reporter and generate the reports
    reporter = SqliteReporter(scriptArgs.inputFile, scriptArgs.outputPath, scriptArgs.reportType, scriptArgs.queriesData)
    reporter.generate_reports()

    # Log that the report generation is finished
    logging.info( "[{timestamp}]: Report generation is finished \r".format(timestamp=str( datetime.now()) ) )


if __name__ == '__main__':
    main()