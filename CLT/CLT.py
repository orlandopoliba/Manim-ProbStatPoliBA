# Manim slide to explain the Central Limit Theorem

from manim import *
import numpy as np
from manim_slides import Slide

class CLT(Slide):
  def construct(self):
    
    title = Tex("Legge della media campionaria").to_edge(UP)
    
    x_min = 0 # -3
    x_max = 1 # 3
    y_max = 10 # 1/np.sqrt(2*np.pi) + 0.2
    n_bins = 20  
    dx = (x_max-x_min)/n_bins
    
    def get_figure(x_min,x_max,dx,y_max):
      figure = VGroup()
      dy = y_max/5
      ax = Axes(
        x_range=[x_min, x_max, dx], 
        x_length=13,
        y_range=[0, y_max, dy],
        y_length=4,
        tips=False, 
      ) 
      figure.add(ax)
      figure.scale(0.8).to_edge(DOWN, buff=1)
      ax = figure[0]
      x_nums = VGroup(
        *[
          DecimalNumber()
          .scale(0.75*0.8) 
          .set_value(x_min + h*dx)
          .rotate(PI/2)
          .next_to(ax.c2p(x_min + h*dx, 0), DOWN, buff=0.35)
          for h in range(n_bins+1)
        ]
      )
      y_nums = VGroup(
        *[
          DecimalNumber()
          .scale(0.75*0.8) 
          .set_value(j*dy)
          .next_to(ax.c2p(0,j*dy), LEFT, buff=0.35)
          for j in range(1,5+1)
        ]
      )
      figure.add(x_nums, y_nums)
      return figure
    
    def compute_sample_densities(means, x_min, dx):
      sample_densities = np.zeros(n_bins)
      for i in range(n_bins):
        sample_densities[i] = np.sum((x_min + i*dx < means) & (means < x_min + (i+1)*dx))/( len(means) * dx )
      return sample_densities
    
    def get_bars(figure, x_min, dx, densities=None):
      if densities is None:
        densities = np.zeros(n_bins)
      bars = VGroup()
      ax = figure[0]
      for h in range(n_bins):
        d = densities[h]
        p1 = VectorizedPoint().move_to(ax.c2p(x_min + h*dx, 0))
        p2 = VectorizedPoint().move_to(ax.c2p(x_min + (h+1)*dx, 0))
        p3 = VectorizedPoint().move_to(ax.c2p(x_min + (h+1)*dx, d))
        p4 = VectorizedPoint().move_to(ax.c2p(x_min + h*dx, d))
        points = VGroup(p1, p2, p3, p4)
        bar = Rectangle().replace(points, stretch=True)
        bar.set_style(
          fill_color=[TEAL],
          fill_opacity=1,
          stroke_color=[TEAL_D],
        )
        bars.add(bar)
      return bars
    
    def generate_random_data(n):
      np.random.seed(0)
      data = np.random.rand(n)
      return data
    
    def compute_means(data,n_sample,n_experiments):
      means = np.zeros(n_experiments)
      for i in range(n_experiments):
        means[i] = np.sum(data[i*n_sample:(i+1)*n_sample])/n_sample # ( np.sum(data[i*n_sample:(i+1)*n_sample])/n_sample  - 0.5 ) * np.sqrt(12*n_sample)
      return means
    
    figure = get_figure(x_min,x_max,dx,y_max)
    n_experiments = 1_000
    n_sample = 10
    data = generate_random_data(n_experiments * n_sample)
    means = compute_means(data, n_sample,n_experiments)
    means_densities = compute_sample_densities(means, x_min, dx)
    bars = get_bars(figure, x_min, dx,means_densities)
    
    population = Tex("Popolazione: $X \sim \mathrm{U}(0,1)$, \ Campione: $X_1,\\dots,X_n$ con $n=" + f"{n_sample}" + "$").center().next_to(title,DOWN,buff=0.6).scale(0.8)
    
    result_string = "$\\overline x_n = \\displaystyle \\frac{1}{" + f"{n_sample}" + "}"+ f"({data[0]:.2f}"
    for j in range(1,n_sample):
      result_string += f" + {data[j]:.2f}"
    result_string += f") = {means[0]:.2f}$"
      
    result = Tex(result_string).scale(0.7).center().next_to(population,DOWN,buff=0.3)

    updating_group_1 = VGroup(
      result,
      bars
    )
    
    def update_1(dummy, i):
      result_string = "$\\overline x_n = \\displaystyle \\frac{1}{" + f"{n_sample}" + "}"+ f"({data[i*n_sample]:.2f}"
      for j in range(i*n_sample+1,(i+1)*n_sample):
        result_string += f" + {data[j]:.2f}"
      result_string += f") = {means[i]:.2f}$"
      
      result.become(Tex(result_string).scale(0.7).center().next_to(population,DOWN,buff=0.3))
      current_densities = compute_sample_densities(means[:i+1], x_min, dx)
      bars.become(get_bars(figure, x_min, dx, current_densities))
 
    self.add(title, figure, population, result, bars)
    
    for i in range(2,10):
      self.play(UpdateFromFunc(updating_group_1, lambda dummy: update_1(dummy, i)), run_time=0.1)
      self.next_slide()
    
    self.next_slide()

    for i in range(10,31):
      self.play(UpdateFromFunc(updating_group_1, lambda dummy: update_1(dummy, i)), run_time=0.1)
        
    for j in range(3,21):
      i = j*10 
      self.play(UpdateFromFunc(updating_group_1, lambda dummy: update_1(dummy, i)), run_time=0.1)    
    
    for j in range(2,10):
      i = j*100 
      print(i)
      self.play(UpdateFromFunc(updating_group_1, lambda dummy: update_1(dummy, i)), run_time=0.1)
    
    self.next_slide()
    
    result_string = "$\\overline X_n$"
    new_result = Tex(result_string).scale(0.7).center().next_to(population,DOWN,buff=0.3)
    self.play(
      Transform(result, new_result),
      run_time=1
      )
    
    self.next_slide()
    
    def get_graph(figure):
      ax = figure[0]
      graph = ax.plot(
        lambda x:  np.exp(-(x-0.5)**2/(2*1/12*1/n_sample))/(np.sqrt(1/12*1/n_sample)*np.sqrt(2*np.pi)),
        color=YELLOW_A,
        stroke_opacity=0.8
      )
      return graph
    
    graph = get_graph(figure)
    self.play(Create(graph), run_time=2)
    
    self.wait(1)