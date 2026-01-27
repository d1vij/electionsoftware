import type { RegistrationRepository } from "./repositories/RegistrationRepository";

export class RegistrationService {
    private db: RegistrationRepository;
    public constructor(db: RegistrationRepository) {
        this.db = db;
    }
}
