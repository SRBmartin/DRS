export interface CreateSurveyRequest {
    title: string;
    question: string;
    ending_time: string;
    is_anonymous: boolean;
    emails?: string[];
};