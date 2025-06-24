export interface ComponentSetup {
    text?: string;
    route?: string;
    options?: Array<string>;
    placeholder?: Array<string>;
    getValue?: any;
    setValue?: any;
    id?: any;
    required?: any
}

export interface ImportedComponentSetup extends ComponentSetup {
    type: string;
}

export interface PageSetup {
    name: string,
    description: string,
    components: ImportedComponentSetup[],
    exports: {
        delimiter: string,
        order: string[]
    }
}