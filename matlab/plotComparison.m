function [] = plotComparison( original, generated, dimension, original_set )
%plotComparison Compare original trajectories against generated
%trajectories
%   Given a set of original trajectories and a set of generated
%   trajectories, plot a single dimension of the set against each other

[~,original_time] = size(original); 
original_dim = original(dimension*original_set,1:original_time);

[~,generated_time] = size(generated); 
generated_dim = generated(dimension,1:generated_time);

figure;
plot(1:original_time, original_dim, 1:generated_time, generated_dim)
legend('Original Trajectories', 'Generated Trajectories')


end

