import { useEffect, useState } from 'react';
import { Button, ButtonProps, Col, Row, Typography } from 'antd';
import FunctionOutlined from '@ant-design/icons/FunctionOutlined';
import { BinocularsIcon } from '@/utils/icons';
import CollapseContent from '@/components/pages/home/promptThread/CollapseContent';
import useAnswerStepContent from '@/hooks/useAnswerStepContent';
import { nextTick } from '@/utils/time';
import styled from 'styled-components';
// import axios from 'axios';

const { Text, Paragraph } = Typography;

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

// const buttonStyle = {
//   height: '24px',
//   marginLeft: '8px',
//   paddingTop: '0px',
//   paddingLeft: '7px',
//   paddingRight: '7px',
// };

interface Props {
  fullSql: string;
  isLastStep: boolean;
  isLastThreadResponse: boolean;
  sql: string;
  stepIndex: number;
  summary: string;
  threadResponseId: number;
  onInitPreviewDone: () => void;
}

export default function StepContent(props: Props) {
  const {
    fullSql,
    isLastStep,
    isLastThreadResponse,
    sql,
    stepIndex,
    summary,
    threadResponseId,
    onInitPreviewDone,
  } = props;

  const [toggleSummary, setToggleSummary] = useState(false);
  const [summaryData] = useState<any>(null);
  const [isLoading] = useState(true);
  const { collapseContentProps, previewDataButtonProps, viewSQLButtonProps } =
    useAnswerStepContent({
      fullSql,
      isLastStep,
      sql,
      threadResponseId,
      stepIndex,
      setToggleSummary,
    });

  const stepNumber = stepIndex + 1;

  const autoTriggerPreviewDataButton = async () => {
    await nextTick();
    await previewDataButtonProps.onClick();
    await nextTick();
    onInitPreviewDone();
  };

  // when is the last step of the last thread response, auto trigger preview data button
  useEffect(() => {
    if (isLastStep && isLastThreadResponse) {
      autoTriggerPreviewDataButton();
    }
  }, [isLastStep, isLastThreadResponse]);

  // const getSummary = async () => {
  //   try {
  //     console.log('Looking for this console', {
  //       summary,
  //       collapseContentProps,
  //     });
  //     const response = await axios.post('http://localhost:8888/data-summary', {
  //       user_query: summary,
  //       data: collapseContentProps.previewDataResult.previewData,
  //       sql: collapseContentProps.sql,
  //     });
  //     if (response && response.data) {
  //       console.log('response from summary api', { response });
  //       setSummaryData(response.data);
  //     }
  //   } catch (error) {
  //     console.error('Error occured in function getSummary', { error });
  //   }
  // };

  // const showSummary = async () => {
  //   await getSummary();
  //   setToggleSummary(true);
  //   setIsLoading(false);
  // };

  return (
    <Row
      className={`pb-3${!isLastStep ? ' mb-5 border-b border-gray-3' : ''}`}
      wrap={false}
    >
      <Col className="text-center" flex="28px">
        <div className="gray-8 text-extra-bold">{stepNumber}.</div>
      </Col>
      <Col flex="auto">
        <Paragraph>
          <Text>{summary}</Text>
        </Paragraph>
        <Button
          {...(previewDataButtonProps as ButtonProps)}
          size="small"
          icon={
            <BinocularsIcon
              style={{
                paddingBottom: 2,
                marginRight: 8,
              }}
            />
          }
          data-ph-capture="true"
          data-ph-capture-attribute-name="cta_answer_preview_data"
          data-ph-capture-attribute-step={stepNumber}
          data-ph-capture-attribute-is_last_step={isLastStep}
        />
        <Button
          {...(viewSQLButtonProps as ButtonProps)}
          size="small"
          icon={<FunctionOutlined />}
          data-ph-capture="true"
          data-ph-capture-attribute-name="cta_answer_view_sql"
          data-ph-capture-attribute-step={stepNumber}
          data-ph-capture-attribute-is_last_step={isLastStep}
        />
        {/* <Button onClick={showSummary} style={buttonStyle}>
          Show Summary
        </Button> */}
        {/* {toggleSummary ? (
          isLoading ? ( // Check if data is still loading
            <TextAreaWrapper>
              <StyledTextArea value={'Loading...'} />
            </TextAreaWrapper>
          ) : summaryData?.data?.status_code === 200 ||
            summaryData?.data?.status_code === '200' ? (
            <TextAreaWrapper>
              <StyledTextArea value={summaryData?.data?.message || ''} />
            </TextAreaWrapper>
          ) : (
            <TextAreaWrapper>
              <StyledTextArea value={summaryData?.data?.message || ''} />
            </TextAreaWrapper>
          )
        ) : (
          <CollapseContent
            {...collapseContentProps}
            key={`collapse-${stepNumber}`}
            attributes={{ stepNumber, isLastStep }}
          />
        )} */}
        {toggleSummary ? (
          isLoading ? (
            <TextAreaWrapper>
              <StyledTextArea value={'Loading...'} />
            </TextAreaWrapper>
          ) : summaryData?.status_code === 400 ? (
            <TextAreaWrapper>
              <StyledTextArea
                value={`Ada could not find any relevant data, can you rephrase the question or be more specific?`}
              />
            </TextAreaWrapper>
          ) : (
            <TextAreaWrapper>
              <StyledTextArea value={summaryData?.message || ''} />
            </TextAreaWrapper>
          )
        ) : (
          <CollapseContent
            {...collapseContentProps}
            key={`collapse-${stepNumber}`}
            attributes={{ stepNumber, isLastStep }}
          />
        )}
        {/* {toggleSummary ? (
          summaryData?.data?.status_code === 200 ? (
            <TextAreaWrapper>
              <StyledTextArea value={summaryData?.data?.message || ''} />
            </TextAreaWrapper>
          ) : (
            <TextAreaWrapper>
              <StyledTextArea value={'No summary to display'} />
            </TextAreaWrapper>
          )
        ) : (
          <CollapseContent
            {...collapseContentProps}
            key={`collapse-${stepNumber}`}
            attributes={{ stepNumber, isLastStep }}
          />
        )} */}
      </Col>
    </Row>
  );
}
