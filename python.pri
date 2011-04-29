python {
  isEmpty(DEPLOYDIR) {
    # Optionally specify location of GLEW using the 
    # GLEWDIR env. variable
    PYTHON_DIR = $$(PYTHONDIR)
    isEmpty(PYTHON_DIR) {
      # Default to MacPorts on Mac OS X
      PYTHON_DIR = /usr/include/python2.6
    }
    !isEmpty(PYTHON_DIR) {
      INCLUDEPATH += $$PYTHON_DIR
      LIBS += -L/usr/lib/python2.6
    }
  }

  unix:LIBS += -lpython2.6
  win32:LIBS += -lpython
}
