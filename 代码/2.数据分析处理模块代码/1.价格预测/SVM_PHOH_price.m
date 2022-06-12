clc,clear
%% 导入数据
price_PHOH{1}=xlsread('PHOH.xls','华中地区','C:C'); %读取华中地区PHOH价格
price_PHOH{2}=xlsread('PHOH.xls','华北地区','C:C'); %读取华北地区PHOH价格
price_PHOH{3}=xlsread('PHOH.xls','华东地区','C:C'); %读取华东地区PHOH价格
price_PHOH{4}=xlsread('PHOH.xls','华南地区','C:C'); %读取华南地区PHOH价格
pnum=length(price_PHOH);
place=['华中地区';'华北地区';'华东地区';'华南地区'];

for p=1:pnum
    n=10; % 确定自变量的个数，为10个
    price_data=price_PHOH{p}(1:end-n);
    for i=1:n
        if i==n
            price_label=price_PHOH{p}(i+1:end-n+i); % 确定因变量
        else
            price_data=[price_data,price_PHOH{p}(i+1:end-n+i)];% 确定自变量
        end
    end

    %% 数据的预处理
    price_data=price_data';
    price_label=price_label';
    [P_data,P_dataps]=mapminmax(price_data,1,100); %对price_data归一化到[1,100];
    [P_label,P_labelps]=mapminmax(price_label,1,100);
    P_label=P_label';
    P_data=P_data';

    %% c、g参数的优化选择
    [bestmse,bestc,bestg]=SVMcgForRegress(P_label,P_data,-10,10,-10,10,10,0.5,0.5,0.1);
    disp('打印选择结果');
    str=sprintf('Best Cross Validation MSE = %g Best c = %g Best g = %g',bestmse,bestc,bestg);
    disp(str);

    %% 利用回归预测分析最佳数据进行SVM网络训练
    cmd=[' -c ',num2str(bestc),' -g ',num2str(bestg),' -s 3 -p 0.01 '];
    model = svmtrain(P_label,P_data,cmd);

    [predict_price,mse_price,d_price]=svmpredict(P_label,P_data,model);
    predict_price_reverse=mapminmax('reverse',predict_price,P_labelps);
    res=predict_price_reverse-price_label';
    mse{p}=sum(res.^2)/length(res);
    figure
    plot(res,'ob');
    xlim=get(gca,'xlim'); %gca代表此时的绘图区，'xlim'代表x轴范围
    hold on
    plot(xlim,[0,0],'k-');
    title(place(p,:));
    
    %% 预测后m个数据
    % 预测数据的自变量
    predict_P_data=P_data(end,2);
    for i=1:n-1
        if i==n-1
            predict_P_data=[predict_P_data,P_label(end,1)];
        else
            predict_P_data=[predict_P_data,P_data(end,2+i)];
        end
    end

    m=30; %预测m个数据
    predict_P_label=[];
    for i=1:m
        [P_predict,P_mse,P_d]=svmpredict(1,predict_P_data,model);
        %获得下一个预测数据的因变量
        predict_P_data_b=predict_P_data;
        predict_P_data=predict_P_data(end,2);
        for j=1:n-1
            if j==n-1
                predict_P_data=[predict_P_data,P_predict];
            else
                predict_P_data=[predict_P_data,predict_P_data_b(end,2+j)];
            end
        end
        P_predict=mapminmax('reverse',P_predict,P_labelps);
        predict_P_label=[predict_P_label,P_predict]; %存储预测的数据
    end
    x_p=length(price_PHOH{p});
    figure
    hold on
    plot(price_PHOH{p},'.-');
    plot(x_p:x_p+m,[price_PHOH{p}(end),predict_P_label],'x-');
    legend('原始数据','预测数据');
    title(place(p,:));
    xlabel('时间');
    ylabel('价格/元');
    label=['C',num2str(x_p+2),':','C',num2str(x_p+31)];
%     xlswrite('G:\数学建模\matlab\时间序列\PHOH-yuce.xls',predict_P_label',place(p,:),label);
end





    
    

 