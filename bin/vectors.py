import numpy as np
import numpy.linalg as linalg


def makeUnit(x):
	"""Normalize entire input to norm 1. Not what you want for 2D arrays!"""
	return x / linalg.norm(x)


def xParV(x, v):
	"""Project x onto v. Result will be parallel to v."""
	# (x' * v / norm(v)) * v / norm(v)
	# = (x' * v) * v / norm(v)^2
	# = (x' * v) * v / (v' * v)
	return np.dot(x, v) / np.dot(v, v) * v


def xPerpV(x, v):
	"""Component of x orthogonal to v. Result is perpendicular to v."""
	return x - xParV(x, v)


def xProjectV(x, v):
	"""Project x onto v, returning parallel and perpendicular components
	>> d = xProject(x, v)
	>> np.allclose(d['par'] + d['perp'], x)
	True
	"""
	par = xParV(x, v)
	perp = x - par
	return {'par': par, 'perp': perp}


def rotateAbout(a, b, theta):
	"""Rotate vector a about vector b by theta radians."""
	# Thanks user MNKY at http://math.stackexchange.com/a/1432182/81266
	proj = xProjectV(a, b)
	w = np.cross(b, proj['perp'])
	return (proj['par'] +
			proj['perp'] * np.cos(theta) +
			linalg.norm(proj['perp']) * makeUnit(w) * np.sin(theta))

def find_rotation(old_v, new_v):
	rotation_vector = np.cross(old_v, new_v)/np.linalg.norm(np.cross(old_v, new_v))
	angle_of_rotation = math.atan(np.linalg.norm(np.cross(old_v, new_v))/np.dot(old_v, new_v.T))
	return rotation_vector.tolist(), angle_of_rotation
