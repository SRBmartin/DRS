export interface SurveyResultsResponse {
    status?: number;
    title: string;
    question: string;
    ending_time: string;
    is_anonymous: boolean;
    responses: {
        yes: number;
        no: number;
        "no response": number;
    };
    user_responses: {
        email: string;
        response: string;
    }[];
    message?: string;
}
