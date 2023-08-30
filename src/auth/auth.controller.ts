import { Body, Controller, Get, Param, Post, Put } from '@nestjs/common';
import { ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger';
import { User } from '@prisma/client';
import { AuthService } from './auth.service';
import {
  AccessToken,
  AuthURL,
  ExchangeToken,
  RefreshToken,
  RevokeToken,
  UserDTO,
  UserResponse,
} from './types';

@Controller('auth')
@ApiTags('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @ApiTags('auth')
  @ApiOperation({
    summary: 'Get authorization url from google',
  })
  @ApiResponse({
    status: 200,
    description: 'Returns authorization url',
    type: AuthURL,
  })
  @Get('google')
  async getAuthorizationUrl(): Promise<AuthURL> {
    const options = {
      scopes: [
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/drive', // Google Drive scope
        'https://www.googleapis.com/auth/documents', // Google Docs scope
      ],
    };
    return {
      url: this.authService.getAuthorizationUrl(options),
    };
  }

  @ApiTags('auth')
  @ApiOperation({
    summary: 'Exchange authorization code for access token',
  })
  @ApiResponse({
    status: 200,
    description: 'Returns access token',
    type: AccessToken,
  })
  @Post('exchange-code')
  async exchangeAuthorizationCode(
    @Body() body: ExchangeToken,
  ): Promise<AccessToken> {
    return await this.authService.exchangeAuthorizationCode(body.code);
  }

  @ApiTags('auth')
  @ApiOperation({
    summary: 'Refresh access token',
  })
  @ApiResponse({
    status: 200,
    description: 'Returns access token',
    type: AccessToken,
  })
  @Post('refresh-access-token')
  async refreshAccessToken(@Body() body: RefreshToken): Promise<AccessToken> {
    return this.authService.refreshAccessToken(body.refreshToken);
  }

  @ApiTags('auth')
  @ApiOperation({
    summary: 'Revoke access token',
  })
  @ApiResponse({
    status: 200,
    description: 'Returns void',
  })
  @Post('revoke-token')
  async logout(@Body() body: RevokeToken): Promise<void> {
    return this.authService.revokeToken(body.accessToken);
  }

  @ApiTags('auth')
  @ApiOperation({
    summary: 'Get user details by id',
  })
  @ApiResponse({
    status: 200,
    description: 'Returns user details',
    type: UserResponse,
  })
  @ApiResponse({
    status: 404,
    description: 'User not found',
  })
  @Get('user/:id')
  async getUser(@Param('id') id: string): Promise<User> {
    return this.authService.getUserDetails(id);
  }

  @ApiTags('auth')
  @ApiOperation({
    summary: 'Update user details',
  })
  @ApiResponse({
    status: 200,
    description: 'Returns user details',
    type: UserResponse,
  })
  @ApiResponse({
    status: 404,
    description: 'User not found',
  })
  @Put('user/:id')
  async updateUser(
    @Param('id') id: string,
    @Body()
    user: UserDTO,
  ): Promise<User> {
    return this.authService.updateUserDetails(id, user);
  }
}
