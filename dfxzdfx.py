import logging
import enum

class LogLevel(enum.IntEnum):
	Silent = 0
	Normal = 1
	Verbose = 2
	Debug = 3

	@classmethod
	def getbyname(cls, name):
		lookup = { level.name.lower(): level for level in cls }
		return lookup[name.lower()]

	@classmethod
	def getnames(cls):
		levels = list(cls)
		levels.sort(key = lambda level: int(level))
		return [ level.name for level in levels ]

	@classmethod
	def getbyverbosity(cls, intvalue):
		maxvalue = max(int(level) for level in cls)
		if intvalue > maxvalue:
			intvalue = maxvalue
		return cls(intvalue)


def configure_logging(verbosity_loglevel):
	llvl = LogLevel.getbyverbosity(verbosity_loglevel)

	logging.TRACE = logging.DEBUG - 1
	logging.addLevelName(logging.TRACE, "TRACE")

	logging_loglevel = {
		LogLevel.Silent:	logging.WARNING,
		LogLevel.Normal:	logging.INFO,
		LogLevel.Verbose:	logging.DEBUG,
		LogLevel.Debug:		logging.TRACE,
	}[llvl]

	def __log_trace(self, message, *args, **kwargs):
		if self.isEnabledFor(logging.TRACE):
			self._log(logging.TRACE, message, args, **kwargs)
	logging.Logger.trace = __log_trace

	logging.basicConfig(format = " {name:>20s} [{levelname:.1s}]: {message}", style = "{", level = logging_loglevel)

if __name__ == "__main__":
	configure_logging(LogLevel.Debug)

	log = logging.getLogger("llpdf.foobar.barfoo")
	log.error("This is an error")
	log.warning("This is a warning")
	log.info("This is an information")
	log.debug("This is debug drivel")
	log.trace("Trace message")

	logger = logging.getLogger(__file__)
	logger.warning("foo bar")

	print(LogLevel.getbyname("nOrMaL"))
	print(LogLevel.getnames())