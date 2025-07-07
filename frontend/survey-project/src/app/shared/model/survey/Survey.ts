import { User } from "../user/user";

export interface Survey{
    id: string;
    user_id: string;
    title: string;
    question: string;
    created_time: Date;
    ending_time: Date;
    is_anonymous: boolean;
    user_ended: boolean;

    user?: User;
};