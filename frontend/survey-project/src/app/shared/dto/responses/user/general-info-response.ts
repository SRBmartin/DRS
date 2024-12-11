import { User } from '../../../model/user/user';

export interface GeneralInfoResponse {
    data?: User;
    message?: string;
    status?: string;      
}
