import { ApiProperty } from "@nestjs/swagger"

export class StringTypeRequestBody {
    @ApiProperty({
        description: 'Type of the template',
      })
    templateType: TemplateType
    @ApiProperty({
        description: 'Input options',
    })
    inputType: StringInputType
    @ApiProperty({
        description: 'Template to be rendered',
    })
    template?: String
    @ApiProperty({
        description: 'JWT token if google doc',
    })
    token?: String
    @ApiProperty({
        description: 'Variables to be replaced in template',
    })
    payload?: JSON
    outputType: OutputType
    deliveryOptions?: DeliveryOptions
    storageOptions?: StorageOptions
}

export enum TemplateType {
    ID="ID",
    EJS="EJS",
    JINJA="JINJA",
    JSTL="JSTL",
    STATIC="STATIC",
}

export enum InputType {
    STRING="STRING",
    FILE="FILE",
    URL="URL",
}

export enum StringInputType {
    PDFMAKE="PDFMAKE",
    GOOGLEDOC="GOOGLEDOC",
    MARKDOWN="MARKDOWN",
    MERMAID="MERMAID",
    TEMPLATOR="TEMPLATOR"
}

export enum OutputTypeOptions {
    SHORTURL="SHORTURL",
    WEBPAGE="WEBPAGE",
}

export enum OutputType {
    png="png",
    jpeg="jpeg",
    html="html",
    pdf="pdf",
    qr="qr",
}

export interface OutputOptions {
    type: OutputType,
    output: OutputTypeOptions
}

export enum DeliveryType {
    WEBHOOK="WEBHOOK",
    EMAIL="EMAIL",
}

export interface DeliveryTypeOptions {
    // TODO
}

export interface DeliveryOptions {
    type: DeliveryType
    options: DeliveryTypeOptions
}

export enum StorageType {
    S3="S3",
    Minio="Minio",
    Dropbox="Dropbox",
    GoogleDrive="GoogleDrive"
}

export interface StorageOptions {
    // TODO
}

export interface StorageOptions {
    type: StorageType
    options: StorageOptions
}