# Manim slide to compare the histogram of the density of frequencies of the data with the density of frequencies of a continous Gamma distribution

import numpy as np
from manim import *
from scipy.stats import gamma
from manim_slides import Slide 

class Density_2(Slide):
  
  def construct(self):
    
    title = Tex("Funzione di densità di probabilità").to_edge(UP)
    
    x_max = 5
    n_bins = 20
    dx = x_max/n_bins
    
    a = 2
    beta = 1.5
    
    def get_figure():
      figure = VGroup()
      ax = Axes(
        x_range=[0, x_max, dx], 
        x_length=8,
        y_range=[0, 0.8],
        y_length=4,
        tips=False, 
      ) 
      x_nums = VGroup(
        *[
          DecimalNumber()
          .scale(0.75) 
          .set_value(i*dx)
          .rotate(PI/2)
          .next_to(ax.c2p(i*dx, 0), DOWN, buff=0.35)
          for i in range(n_bins+1)
        ]
      )
      
      figure.add(ax, x_nums)
      figure.to_edge(DL, buff=0.6)
      return figure
    
    def get_graph(figure):
      ax = figure[0]
      graph = ax.plot(
        lambda x: gamma.pdf(x, a, loc=0, scale=1/beta),
        color=YELLOW_A
      )
      return graph
    
    def compute_sample_densities(data):
      sample_densities = np.zeros(n_bins)
      for i in range(n_bins):
        sample_densities[i] = np.sum((i*dx < data) & (data < (i+1)*dx))/( len(data) * dx )
      return sample_densities
        
    def get_bars(figure, densities=None):
      if densities is None:
        densities = np.zeros(n_bins)
      bars = VGroup()
      ax = figure[0]
      for i in range(n_bins):
        d = densities[i]
        p1 = VectorizedPoint().move_to(ax.c2p(i*dx, 0))
        p2 = VectorizedPoint().move_to(ax.c2p((i+1)*dx, 0))
        p3 = VectorizedPoint().move_to(ax.c2p((i+1)*dx, d))
        p4 = VectorizedPoint().move_to(ax.c2p(i*dx, d))
        points = VGroup(p1, p2, p3, p4)
        bar = Rectangle().replace(points, stretch=True)
        bar.set_style(
          fill_color=[TEAL],
          fill_opacity=1,
          stroke_color=[TEAL_D],
        )
        bars.add(bar)
      return bars
    
    def generate_random_data(n, a, beta):
      data = gamma.rvs(a, loc=0, scale=1/beta, size=n)
      return data
    
    text = VGroup()
    text_experiment_counter = Tex("Esperimento numero: ").scale(0.6)
    text.add(text_experiment_counter)
    text.arrange(DOWN, center=False, aligned_edge=LEFT)  
    text.to_edge(RIGHT, buff=2)
    experiment_counter = Tex(f"{0}").scale(0.6).next_to(text_experiment_counter, RIGHT)
 
    
    figure = get_figure()
    graph = get_graph(figure)
    n_experiments = 5_000
    data = generate_random_data(n_experiments, a, beta)
 
    bars = get_bars(figure)
    result = Tex("-").center().next_to(title,DOWN,buff=0.6)
    
    self.add(title, 
             figure,
             result, 
             bars, 
             text, 
             experiment_counter,
             )
    
    updating_group = VGroup(
      result,
      bars,
      experiment_counter
    )
    
    def update(dummy, current_data, i, jump=False):
      if jump:
        result.become(Tex(f"({jump} esiti)").center().next_to(title,DOWN,buff=0.6)) 
      else:
        result.become(Tex(f"{current_data[len(current_data)-1]:.4f}").center().next_to(title,DOWN,buff=0.6))
      current_densities = compute_sample_densities(np.array(current_data))
      bars.become(get_bars(figure, current_densities))
      experiment_counter.become(Tex(f"{len(current_data)}").scale(0.6).next_to(text_experiment_counter, RIGHT))      
    
    for i in range(1, 2):
      current_data = data[range(i*100)]
      print("Generating experiment ", i*100)
      self.play(UpdateFromFunc(updating_group, lambda dummy: update(dummy, current_data, i, jump=100)), run_time=0.1)
    for i in range(2, 51):
      current_data = data[range(i*100)]
      print("Generating experiment ", i*100)
      self.play(UpdateFromFunc(updating_group, lambda dummy: update(dummy, current_data, i, jump=100)), run_time=0.1)
    self.next_slide()
    
    self.play(Create(graph), run_time=2)
    
    self.wait(1)