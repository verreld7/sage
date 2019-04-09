## -*- encoding: utf-8 -*-
"""
This file (./graphique_doctest.sage) was *autogenerated* from ./graphique.tex,
with sagetex.sty version 2011/05/27 v2.3.1.
It contains the contents of all the sageexample environments from this file.
You should be able to doctest this file with:
sage -t ./graphique_doctest.sage
It is always safe to delete this file; it is not used in typesetting your
document.

Sage example in ./graphique.tex, line 18::

  sage: reset()

Sage example in ./graphique.tex, line 61::

  sage: plot(x * sin(1/x), x, -2, 2, plot_points=500)
  Graphics object consisting of 1 graphics primitive

Sage example in ./graphique.tex, line 156::

  sage: def p(x, n):
  ....:     return(taylor(sin(x), x, 0, n))
  sage: xmax = 15 ; n = 15
  sage: g = plot(sin(x), x, -xmax, xmax)
  sage: for d in range(n):  # long time
  ....:   g += plot(p(x, 2 * d + 1), x, -xmax, xmax,\
  ....:     color=(1.7*d/(2*n), 1.5*d/(2*n), 1-3*d/(4*n)))
  sage: g.show(ymin=-2, ymax=2)

Sage example in ./graphique.tex, line 237::

  sage: f2(x) = 1; f1(x) = -1
  sage: f = piecewise([[(-pi,0),f1],[(0,pi),f2]])
  sage: S = f.fourier_series_partial_sum(20,pi)
  sage: g = plot(S, x, -8, 8, color='blue')
  sage: saw(x) = x - 2 * pi * floor((x + pi) / (2 * pi))
  sage: g += plot(saw(x) / abs(saw(x)), x, -8, 8, color='red')
  sage: g
  Graphics object consisting of 2 graphics primitives

Sage example in ./graphique.tex, line 311::

  sage: t = var('t')
  sage: x = cos(t) + cos(7*t)/2 + sin(17*t)/3
  sage: y = sin(t) + sin(7*t)/2 + cos(17*t)/3
  sage: g = parametric_plot((x, y), (t, 0, 2*pi))
  sage: g.show(aspect_ratio=1)

Sage example in ./graphique.tex, line 364::

  sage: t = var('t'); n = 20/19
  sage: g1 = polar_plot(1+2*cos(n*t),(t,0,n*36*pi),plot_points=5000)
  sage: g2 = polar_plot(1+1/3*cos(n*t),(t,0,n*36*pi),plot_points=5000)
  sage: g1.show(aspect_ratio=1); g2.show(aspect_ratio=1)

Sage example in ./graphique.tex, line 500::

  sage: bar_chart([randrange(15) for i in range(20)])
  Graphics object consisting of 1 graphics primitive
  sage: bar_chart([x^2 for x in range(1,20)], width=0.2)
  Graphics object consisting of 1 graphics primitive

Sage example in ./graphique.tex, line 550::

  sage: liste = [10 + floor(10*sin(i)) for i in range(100)]
  sage: bar_chart(liste)
  Graphics object consisting of 1 graphics primitive
  sage: finance.TimeSeries(liste).plot_histogram(bins=20)
  Graphics object consisting of 20 graphics primitives

Sage example in ./graphique.tex, line 714::

  sage: n, l, x, y = 10000, 1, 0, 0; p = [[0, 0]]
  sage: for k in range(n):
  ....:     theta = (2 * pi * random()).n(digits=5)
  ....:     x, y = x + l * cos(theta), y + l * sin(theta)
  ....:     p.append([x, y])
  sage: g1 = line([p[n], [0, 0]], color='red', thickness=2)
  sage: g1 += line(p, thickness=.4); g1.show(aspect_ratio=1)

Sage example in ./graphique.tex, line 777::

  sage: length = 200; n = var('n')
  sage: u = lambda n: n * sqrt(2)
  sage: z = lambda n: exp(2 * I * pi * u(n)).n()
  sage: vertices = [CC(0, 0)]
  sage: for n in range(1, length):
  ....:     vertices.append(vertices[n - 1] + CC(z(n)))
  sage: line(vertices).show(aspect_ratio=1)

Sage example in ./graphique.tex, line 968::

  sage: x = var('x'); y = function('y')
  sage: DE = x*diff(y(x), x) == 2*y(x) + x^3
  sage: desolve(DE, [y(x),x])
  (_C + x)*x^2
  sage: sol = []
  sage: for i in srange(-2, 2, 0.2):
  ....:     sol.append(desolve(DE, [y(x), x], ics=[1, i]))
  ....:     sol.append(desolve(DE, [y(x), x], ics=[-1, i]))
  sage: g = plot(sol, x, -2, 2)
  sage: y = var('y')
  sage: g += plot_vector_field((x, 2*y+x^3), (x,-2,2), (y,-1,1))
  sage: g.show(ymin=-1, ymax=1)

Sage example in ./graphique.tex, line 1029::

  sage: x = var('x'); y = function('y')
  sage: DE = x*diff(y(x), x) == 2*y(x) + x^3
  sage: g = Graphics()             # creates an empty graph
  sage: for i in srange(-2, 2, 0.2):  # long time
  ....:     g += line(desolve_rk4(DE, y(x), ics=[1, i],\
  ....:                       step=0.05, end_points=[0,2]))
  ....:     g += line(desolve_rk4(DE, y(x), ics=[-1, i],\
  ....:                       step=0.05, end_points=[-2,0]))
  sage: y = var('y')
  sage: g += plot_vector_field((x, 2*y+x^3), (x,-2,2), (y,-1,1))
  sage: g.show(ymin=-1, ymax=1)

Sage example in ./graphique.tex, line 1120::

  sage: import scipy; from scipy import integrate
  sage: f = lambda y, t: - cos(y * t)
  sage: t = srange(0, 5, 0.1); p = Graphics()
  sage: for k in srange(0, 10, 0.15):
  ....:       y = integrate.odeint(f, k, t)
  ....:       p += line(zip(t, flatten(y)))
  sage: t = srange(0, -5, -0.1); q = Graphics()
  sage: for k in srange(0, 10, 0.15):
  ....:       y = integrate.odeint(f, k, t)
  ....:       q += line(zip(t, flatten(y)))
  sage: y = var('y')
  sage: v = plot_vector_field((1, -cos(x*y)), (x,-5,5), (y,-2,11))
  sage: g = p + q + v; g.show()

Sage example in ./graphique.tex, line 1229::

  sage: import scipy; from scipy import integrate
  sage: a, b, c, d = 1., 0.1, 1.5, 0.75
  sage: def dX_dt(X, t=0):             # returns the population variation
  ....:     return [a*X[0] - b*X[0]*X[1], -c*X[1] + d*b*X[0]*X[1]]
  sage: t = srange(0, 15, .01)                               # time scale
  sage: X0 = [10, 5]         # initial conditions: 10 rabbits and 5 foxes
  sage: X = integrate.odeint(dX_dt, X0, t)           # numerical solution
  sage: rabbits, foxes =  X.T                # shortcut for X.transpose()
  sage: p = line(zip(t, rabbits), color='red')  # number of rabbits graph
  sage: p += text("Rabbits",(12,37), fontsize=10, color='red')
  sage: p += line(zip(t, foxes), color='blue')           # idem for foxes
  sage: p += text("Foxes",(12,7), fontsize=10, color='blue')
  sage: p.axes_labels(["time", "population"]); p.show(gridlines=True)

Sage example in ./graphique.tex, line 1266::

  sage: n = 11;  L = srange(6, 18, 12 / n); R = srange(3, 9, 6 / n)
  sage: CI = list(zip(L, R))           # list of initial conditions
  sage: def g(x,y):
  ....:     v = vector(dX_dt([x, y]))  # for a nicer graph, we
  ....:     return v/v.norm()          # normalise the vector field
  sage: x, y = var('x, y')
  sage: q = plot_vector_field(g(x, y), (x, 0, 60), (y, 0, 36))
  sage: for j in range(n):
  ....:     X = integrate.odeint(dX_dt, CI[j], t)        # resolution
  ....:     q += line(X, color=hue(.8-float(j)/(1.8*n))) # graph plot
  sage: q.axes_labels(["rabbits","foxes"]); q.show()

Sage example in ./graphique.tex, line 1501::

  sage: x, y, t = var('x, y, t')
  sage: alpha(t) = 1; beta(t) = t / 2; gamma(t) = t + t^3 / 8
  sage: env = solve([alpha(t) * x + beta(t) * y == gamma(t),\
  ....:     diff(alpha(t), t) * x + diff(beta(t), t) * y == \
  ....:     diff(gamma(t), t)], [x,y])

Sage example in ./graphique.tex, line 1541::

  sage: f(x) = x^2 / 4
  sage: p = plot(f, -8, 8, rgbcolor=(0.2,0.2,0.4))  # the parabola
  sage: for u in srange(0, 8, 0.1):      # normals to the parabola
  ....:    p += line([[u, f(u)], [-8*u, f(u) + 18]], thickness=.3)
  ....:    p += line([[-u, f(u)], [8*u, f(u) + 18]], thickness=.3)
  sage: p += parametric_plot((env[0][0].rhs(),env[0][1].rhs()),\
  ....:    (t, -8, 8),color='red')             # draws the evolute
  sage: p.show(xmin=-8, xmax=8, ymin=-1, ymax=12, aspect_ratio=1)

Sage example in ./graphique.tex, line 1604::

  sage: t = var('t'); p = 2
  sage: x(t) = t; y(t) = t^2 / (2 * p); f(t) = [x(t), y(t)]
  sage: df(t) = [x(t).diff(t), y(t).diff(t)]
  sage: d2f(t) = [x(t).diff(t, 2), y(t).diff(t, 2)]
  sage: T(t) = [df(t)[0] / df(t).norm(), df[1](t) / df(t).norm()]
  sage: N(t) = [-df(t)[1] / df(t).norm(), df[0](t) / df(t).norm()]
  sage: R(t) = (df(t).norm())^3 / (df(t)[0]*d2f(t)[1]-df(t)[1]*d2f(t)[0])
  sage: Omega(t) = [f(t)[0] + R(t)*N(t)[0], f(t)[1] + R(t)*N(t)[1]]
  sage: g = parametric_plot(f(t), (t,-8,8), color='green',thickness=2)
  sage: for u in srange(.4, 4, .2):
  ....:     g += line([f(t=u), Omega(t=u)], color='red', alpha = .5)
  ....:     g += circle(Omega(t=u), R(t=u), color='blue')
  sage: g.show(aspect_ratio=1,xmin=-12,xmax=7,ymin=-3,ymax=12)

Sage example in ./graphique.tex, line 1781::

  sage: u, v = var('u, v')
  sage: h = lambda u,v: u^2 + 2*v^2
  sage: plot3d(h, (u,-1,1), (v,-1,1), aspect_ratio=[1,1,1])
  Graphics3d Object

Sage example in ./graphique.tex, line 1833::

  sage: f(x, y) = x^2 * y / (x^4 + y^2)
  sage: t, theta = var('t, theta')
  sage: limit(f(t * cos(theta), t * sin(theta)) / t, t=0)
  cos(theta)^2/sin(theta)

Sage example in ./graphique.tex, line 1847::

  sage: solve(f(x,y) == 1/2, y)
  [y == x^2]
  sage: a = var('a'); h = f(x, a*x^2).simplify_rational(); h
  a/(a^2 + 1)

Sage example in ./graphique.tex, line 1861::

  sage: plot(h, a, -4, 4)
  Graphics object consisting of 1 graphics primitive

Sage example in ./graphique.tex, line 1908::

  sage: p = plot3d(f(x,y),(x,-2,2),(y,-2,2),plot_points=[150,150])

Sage example in ./graphique.tex, line 1937::

  sage: for i in range(1,4):
  ....:  p += plot3d(-0.5 + i / 4, (x, -2, 2), (y, -2, 2),\
  ....:               color=hue(i / 10), opacity=.1)

Sage example in ./graphique.tex, line 1956::

  sage: x, y, z = var('x, y, z'); a = 1
  sage: h = lambda x, y, z:(a^2 + x^2 + y^2)^2 - 4*a^2*x^2-z^4
  sage: implicit_plot3d(h, (x,-3,3), (y,-3,3), (z,-2,2),  # long time
  ....:                 plot_points=100)
  Graphics3d Object

Sage example in ./graphique.tex, line 2004::

  sage: line3d([(-10*cos(t)-2*cos(5*t)+15*sin(2*t),\
  ....:          -15*cos(2*t)+10*sin(t)-2*sin(5*t),\
  ....:          10*cos(3*t)) for t in srange(0,6.4,.1)],radius=.5)
  Graphics3d Object

"""

