from pyscad_script import Model
from pyscad import *

# The original way (provided by pyscad).
# This doesn't work, as there is no pyscad.scale or pyscad.translate, but you
# get the idea.
def generate_old():
	cube1 = translate([20, 0, 0], [scale([2, 1, 1], [cube(10)])])
	cube2 = cube(10)
	print "### generate_old"
	print union([cube1, cube2]).to_source()


# Using pyscad_script.
def generate_new():
	model = Model()
	
	with model.union():
		with model.translate([20, 0, 0]).scale([2, 1, 1]):
			model.cube(10)
		model.cube(10)
	
	print "### generate_new"
	print model.get_object().to_source()


# Example of defining an operator
# (a module with child nodes, in OpenSCAD terms).
def my_intersect(model, p, children):
	print p
	with model.intersection():
		model.add(*children)

# A test of the above operator.
def generate_with_my_operator():
	model = Model()
	
	with model.push(my_intersect, 5):
		model.sphere(3, center=(10,10,10))
		model.cube(10)
	
	print "### generate_with_my_operator"
	print model.get_object().to_source()


if __name__ == "__main__":
	generate_new()
	generate_with_my_operator()
