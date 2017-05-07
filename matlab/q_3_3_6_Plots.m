% Plots for 3.2.6
close all;

[original, ~] = load_htkdata('../original/cmp/utt1.cmp');

[generated, ~] = load_traj('../traj/utt1.mcep',60);

[generatedAligned, ~] = load_traj('../traj-dur/utt1.mcep',60);

[dist, ix, iy] = dtw(original(1,:),generated(1,:));
generatedDim1 = generated(1,:);
generatedAlignedDTW = generatedDim1(iy);
originalDim1 = original(1,:);
originalAlignedDTW = originalDim1(ix);

% Comparison of original against traj
figure;
plot(original(1,:));
hold on;
plot(generated(1,4:end));
legend('Original', 'HTS');
xlabel('Frame');

% Comparison of original against traj-dur
figure;
plot(original(1,:));
hold on;
plot(generatedAligned(1,:));
legend('Original', 'HTS');
xlabel('Frame');

% Comparison of DTW of original against traj
figure;
plot(originalAlignedDTW);
hold on;
plot(generatedAlignedDTW);
legend('Original', 'HTS');
xlabel('Frame');