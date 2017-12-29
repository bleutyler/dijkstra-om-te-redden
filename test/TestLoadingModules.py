import unittest

class TestLoadingModules( unittest.TestCase ):
	def _test_module( self, module_name ):
		try:
			__import__( module_name )
		except ImportError:
			self.fail( 'Failed to load module: ' + module_name )
		
	def test_loading_modules( self ):
		list_of_modules = [ 'logging', 'sys', 'os', 're', 'copy' ]  
		for mod in list_of_modules:
			self._test_module( mod )

