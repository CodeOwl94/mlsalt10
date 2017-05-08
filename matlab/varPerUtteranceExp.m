function [] = varPerUtteranceExp( dimension )
%compareEachUtterance Compare information across different utterances
%   Given the datasets, plot the global variances for the given dimension
%   for the different models considered. 
close all;

histMatrix1 = zeros([9 3]); % Original, ExpGV, ExpAltGV

for ii=1:9 
    [original,~] = load_htkdata(strcat('../original/cmp/utt',int2str(ii),'.cmp'));
    original = original(dimension,:);

    fileID = fopen(strcat('../allTraj/traj/utt',int2str(ii),'/dim',int2str(dimension),'/trajExpertGV.txt'));
    expertGV = fscanf(fileID, '%f');
    fclose(fileID);
    
    fileID = fopen(strcat('../allTraj/traj/utt',int2str(ii),'/dim',int2str(dimension),'/trajExpertAltGV.txt'));
    expertAltGV = fscanf(fileID, '%f');
    fclose(fileID);
    
    histMatrix1(ii,:) = [var(original), var(expertGV), var(expertAltGV)];
    
end

% Plot the results
bar(histMatrix1);
xlabel('Utterance');
ylabel('Variance');
%ylim([0 1e-3]);
legend('Original', 'Expert GV 1', 'Expert GV 2');

end