import pyscad

# Utility functions for adding modifiers and primitives to the Model class.
def make_modifier(mod):
	def f(model, *args, **kwargs):
		model.add(mod(*args, **kwargs))
	def g(self, *args, **kwargs):
		self.push(f, *args, **kwargs)
		return self
	return g

def make_primitive(obj):
	def f(self, *args, **kwargs):
		self.add(obj(*args, **kwargs))
	return f


class Model(object):
	
	def __init__(self):
		# The None values are used as a marker that is added every time a with
		# statement is entered. This way, we can do multiple pushes, and always pop
		# back to the intended place.
		self.stack = [(None, None, None, []), None]
	
	def __enter__(self):
		# A marker so that we know where to 'pop' to upon __exit__.
		self.stack.append(None)
		return self
	
	def push(self, f, *args, **kwargs):
		"""Push an operator into the stack.
		Don't call this outside of a while statement,
		it won't do the right thing."""
		self.stack.append((f, args, kwargs, []))
		# Allow chaining.
		return self
	
	def pop(self):
		"""Apply the operator on the top of the stack."""
		f, f_args, f_kwargs, f_extras = self.stack.pop()
		f(self, children=f_extras, *f_args, **f_kwargs)
	
	def __exit__(self, *args):
		# Remove the None value added by __enter__.
		self.stack.pop()
		
		# Remove all the operators pushed at the start
		# of this with statement.
		while self.stack[-1] is not None:
			self.pop()
		
		# Let any exception propagate.
		return False
	
	def top_frame(self):
		"""Get the top not-None frame of the stack."""
		return [f for f in self.stack if f is not None][-1]
	
	def add(self, *objs):
		"""Add some objects to this model."""
		for o in objs:
			self.top_frame()[3].append(o)
	
	def get_objects(self):
		"""Get all the objects added to the model."""
		return self.top_frame()[3]
	
	def get_object(self):
		"""Get a single object."""
		objects = self.get_objects()
		assert len(objects) == 1
		return objects[0]
	
	# Boolean operators.
	intersection = make_modifier(pyscad.intersection)
	union = make_modifier(pyscad.union)
	difference = make_modifier(pyscad.difference)
	
	# Transforms.
	scale = make_modifier(pyscad.scale)
	translate = make_modifier(pyscad.translate)
	
	# Primitives.
	cube = make_primitive(pyscad.cube)
	sphere = make_primitive(pyscad.sphere)
	cylinder = make_primitive(pyscad.cylinder)
