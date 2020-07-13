__copyright__ = """
Copyright (C) 2020 University of Illinois Board of Trustees
"""

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import logging
import numpy as np
import numpy.linalg as la  # noqa
import pyopencl.array as cla  # noqa

from mirgecom.steppers import euler_flow_stepper
from mirgecom.boundary import PrescribedBoundary
from mirgecom.initializers import Vortex2D
from mirgecom.eos import IdealSingleGas
from meshmode.mesh import BTAG_ALL, BTAG_NONE  # noqa


def main():
    dim = 2
    nel_1d = 16
    logger = logging.getLogger(__name__)

    from meshmode.mesh.generation import generate_regular_rect_mesh

    mesh = generate_regular_rect_mesh(
        a=(-5.0,) * dim, b=(5.0,) * dim, n=(nel_1d,) * dim
    )

    order = 3
    exittol = .09
    t_final = 0.1
    cfl = 1.0
    vel = np.zeros(shape=(dim,))
    orig = np.zeros(shape=(dim,))
    vel[:dim] = 1.0
    dt = .001
    initializer = Vortex2D(center=orig, velocity=vel)
    casename = 'Vortex'
    boundaries = {BTAG_ALL: PrescribedBoundary(initializer)}
    eos = IdealSingleGas()
    t = 0
    flowparams = {'dim': dim, 'dt': dt, 'order': order, 'time': t,
                  'boundaries': boundaries, 'initializer': initializer,
                  'eos': eos, 'casename': casename, 'mesh': mesh,
                  'tfinal': t_final, 'exittol': exittol, 'cfl': cfl,
                  'constantcfl': False, 'nstatus': 10}

    maxerr = euler_flow_stepper(flowparams)
    logger.info(f'{casename} maxerr = {maxerr}')


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()

# vim: foldmethod=marker