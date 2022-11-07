export interface TextSetup {
    text: string;
    placeholder: Array<string>;
    route: string;
}

export interface DropDownSetup extends TextSetup {
    options: Array<string>
}