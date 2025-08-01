import clsx from 'clsx';
import styled from 'styled-components';
import { useEffect, useMemo, useState } from 'react';
import { Skeleton } from 'antd';
import BulbOutlined from '@ant-design/icons/BulbOutlined';
// import { makeIterable } from '@/utils/iteration';
import {
  RecommendedQuestionsTask,
  RecommendedQuestionsTaskStatus,
} from '@/apollo/client/graphql/__types__';
import axios from 'axios';

interface Props {
  items: { question: string; sql: string }[];
  loading?: boolean;
  error?: {
    shortMessage?: string;
    code?: string;
    message?: string;
    stacktrace?: string[];
  };
  className?: string;
  onSelect?: ({ question, sql }: { question: string; sql: string }) => void;
  previewDataForSuggestion?: any;
}

const StyledSkeleton = styled(Skeleton)`
  padding: 4px 0;
  .ant-skeleton-paragraph {
    margin-bottom: 0;
    li {
      height: 14px;
      + li {
        margin-top: 12px;
      }
    }
  }
`;

const TextAreaWrapper = styled.div`
  max-width: 100%;
  width: 100%;
  padding: 20px;
  display: flex;
  justify-content: center;
`;

const StyledTextArea = styled.textarea`
  width: 100%;
  height: 400px;
  padding: 10px;
  font-size: 14px;
  font-family: 'Arial', sans-serif;
  border: 1px solid #ccc;
  border-radius: 8px;
  resize: vertical; /* Allow the user to resize vertically */
  box-sizing: border-box; /* Includes padding and border in width/height calculation */
  background-color: #f9f9f9;
  color: #333;
  line-height: 1.5;
  overflow-y: auto; /* Make it scrollable if the content exceeds height */
  transition:
    border-color 0.3s ease,
    box-shadow 0.3s ease;

  &:focus {
    border-color: #007bff;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
    outline: none;
  }
`;

export const getRecommendedQuestionProps = (
  data: RecommendedQuestionsTask,
  show = true,
) => {
  if (!data || !show) return { show: false };
  const questions = (data?.questions || []).slice(0, 3).map((item) => ({
    question: item.question,
    sql: item.sql,
  }));
  const loading = data?.status === RecommendedQuestionsTaskStatus.GENERATING;
  return {
    show: loading || questions.length > 0,
    state: {
      items: questions,
      loading,
      error: data?.error,
    },
  };
};

// const QuestionItem = (props: {
//   index: number;
//   question: string;
//   sql: string;
//   onSelect?: ({ question, sql }: { question: string; sql: string }) => void;
// }) => {
//   const { index, question, sql, onSelect } = props;
//   return (
//     <div className={clsx(index > 0 && 'mt-1')}>
//       <span
//         className="cursor-pointer hover:text"
//         onClick={() => onSelect({ question, sql })}
//       >
//         {question}
//       </span>
//     </div>
//   );
// };
// const QuestionList = makeIterable(QuestionItem);

export default function RecommendedQuestions(props: Props) {
  const { items, loading, className, previewDataForSuggestion } = props;
  const [summaryData, setSummaryData] = useState<any>();

  const data = useMemo(
    () => items.map(({ question, sql }) => ({ question, sql })),
    [items],
  );

  const getSummary = async () => {
    try {
      console.log('Looking for this console', {
        data,
        previewDataForSuggestion,
      });
      const response = await axios.post('http://localhost:8000/data-summary', {
        user_query: data,
        data: previewDataForSuggestion.previewData,
        sql: previewDataForSuggestion.sql,
      });
      console.log('response from summary api', { response });
      setSummaryData(response.data.message);
    } catch (error) {
      console.error('Error occured in function getSummary', { error });
    }
  };

  useEffect(() => {
    console.log('Looking for previewDataForSuggestion ', {
      previewDataForSuggestion,
    });
    if (previewDataForSuggestion) {
      getSummary();
    }
  }, []);

  return (
    <div className={clsx('bg-gray-2 rounded p-3', className)}>
      <div className="mb-2">
        <BulbOutlined className="mr-1 gray-6" />
        <b className="text-semi-bold text-sm gray-7">Data Summary</b>
      </div>
      <div className="pl-1 gray-8">
        <StyledSkeleton
          active
          loading={loading}
          paragraph={{ rows: 3 }}
          title={false}
        >
          <TextAreaWrapper>
            <StyledTextArea value={summaryData} />
          </TextAreaWrapper>
          {/* <QuestionList data={data} onSelect={onSelect} /> */}
        </StyledSkeleton>
      </div>
    </div>
  );
}
