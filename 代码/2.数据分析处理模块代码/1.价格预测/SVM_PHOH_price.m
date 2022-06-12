clc,clear
%% ��������
price_PHOH{1}=xlsread('PHOH.xls','���е���','C:C'); %��ȡ���е���PHOH�۸�
price_PHOH{2}=xlsread('PHOH.xls','��������','C:C'); %��ȡ��������PHOH�۸�
price_PHOH{3}=xlsread('PHOH.xls','��������','C:C'); %��ȡ��������PHOH�۸�
price_PHOH{4}=xlsread('PHOH.xls','���ϵ���','C:C'); %��ȡ���ϵ���PHOH�۸�
pnum=length(price_PHOH);
place=['���е���';'��������';'��������';'���ϵ���'];

for p=1:pnum
    n=10; % ȷ���Ա����ĸ�����Ϊ10��
    price_data=price_PHOH{p}(1:end-n);
    for i=1:n
        if i==n
            price_label=price_PHOH{p}(i+1:end-n+i); % ȷ�������
        else
            price_data=[price_data,price_PHOH{p}(i+1:end-n+i)];% ȷ���Ա���
        end
    end

    %% ���ݵ�Ԥ����
    price_data=price_data';
    price_label=price_label';
    [P_data,P_dataps]=mapminmax(price_data,1,100); %��price_data��һ����[1,100];
    [P_label,P_labelps]=mapminmax(price_label,1,100);
    P_label=P_label';
    P_data=P_data';

    %% c��g�������Ż�ѡ��
    [bestmse,bestc,bestg]=SVMcgForRegress(P_label,P_data,-10,10,-10,10,10,0.5,0.5,0.1);
    disp('��ӡѡ����');
    str=sprintf('Best Cross Validation MSE = %g Best c = %g Best g = %g',bestmse,bestc,bestg);
    disp(str);

    %% ���ûع�Ԥ�����������ݽ���SVM����ѵ��
    cmd=[' -c ',num2str(bestc),' -g ',num2str(bestg),' -s 3 -p 0.01 '];
    model = svmtrain(P_label,P_data,cmd);

    [predict_price,mse_price,d_price]=svmpredict(P_label,P_data,model);
    predict_price_reverse=mapminmax('reverse',predict_price,P_labelps);
    res=predict_price_reverse-price_label';
    mse{p}=sum(res.^2)/length(res);
    figure
    plot(res,'ob');
    xlim=get(gca,'xlim'); %gca�����ʱ�Ļ�ͼ����'xlim'����x�᷶Χ
    hold on
    plot(xlim,[0,0],'k-');
    title(place(p,:));
    
    %% Ԥ���m������
    % Ԥ�����ݵ��Ա���
    predict_P_data=P_data(end,2);
    for i=1:n-1
        if i==n-1
            predict_P_data=[predict_P_data,P_label(end,1)];
        else
            predict_P_data=[predict_P_data,P_data(end,2+i)];
        end
    end

    m=30; %Ԥ��m������
    predict_P_label=[];
    for i=1:m
        [P_predict,P_mse,P_d]=svmpredict(1,predict_P_data,model);
        %�����һ��Ԥ�����ݵ������
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
        predict_P_label=[predict_P_label,P_predict]; %�洢Ԥ�������
    end
    x_p=length(price_PHOH{p});
    figure
    hold on
    plot(price_PHOH{p},'.-');
    plot(x_p:x_p+m,[price_PHOH{p}(end),predict_P_label],'x-');
    legend('ԭʼ����','Ԥ������');
    title(place(p,:));
    xlabel('ʱ��');
    ylabel('�۸�/Ԫ');
    label=['C',num2str(x_p+2),':','C',num2str(x_p+31)];
%     xlswrite('G:\��ѧ��ģ\matlab\ʱ������\PHOH-yuce.xls',predict_P_label',place(p,:),label);
end





    
    

 