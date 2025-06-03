export interface SurveyResultsResponse {
    status?: number;
    title: string;
    question: string;
    ending_time: string;
    user_ended: boolean;
    is_anonymous: boolean;
    responses: {
        yes: number;
        no: number;
        no_response: number;
    };
    user_responses: {
        email: string;
        response: string;
    }[];
    message?: string;
}
