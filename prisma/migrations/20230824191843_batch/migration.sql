-- CreateEnum
CREATE TYPE "TemplateType" AS ENUM ('JINJA', 'EJS', 'JSTL');

-- CreateEnum
CREATE TYPE "BatchStatus" AS ENUM ('submitted', 'queued', 'running', 'done', 'aborted');

-- CreateEnum
CREATE TYPE "OutputType" AS ENUM ('png', 'jpeg', 'html', 'pdf', 'qr');

-- CreateTable
CREATE TABLE "Template" (
    "id" SERIAL NOT NULL,
    "content" TEXT NOT NULL,
    "templateType" "TemplateType" NOT NULL,

    CONSTRAINT "Template_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Batch" (
    "id" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "templateType" "TemplateType" NOT NULL,
    "templateID" INTEGER NOT NULL,
    "payload" JSONB[],
    "status" "BatchStatus" NOT NULL DEFAULT 'submitted',
    "output" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "outputType" "OutputType" NOT NULL DEFAULT 'pdf',

    CONSTRAINT "Batch_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "User" (
    "id" SERIAL NOT NULL,
    "username" TEXT NOT NULL,
    "firstName" TEXT NOT NULL,
    "lastName" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "phone" TEXT NOT NULL,
    "userStatus" INTEGER NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_username_key" ON "User"("username");

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- AddForeignKey
ALTER TABLE "Batch" ADD CONSTRAINT "Batch_templateID_fkey" FOREIGN KEY ("templateID") REFERENCES "Template"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
