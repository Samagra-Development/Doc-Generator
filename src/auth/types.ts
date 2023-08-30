import { ApiProperty } from '@nestjs/swagger';

export interface OAuthService {
  getAuthorizationUrl(options: AuthorizationOptions): string;
  exchangeAuthorizationCode(authorizationCode: string): Promise<AccessToken>;
  refreshAccessToken(refreshToken: string): Promise<AccessToken>;
  revokeToken(token: string): Promise<void>;
}

export interface AuthorizationOptions {
  scopes: string[];
  state?: string;
  // Additional provider-specific options can be added here
}

export class AccessToken {
  @ApiProperty({
    description: 'Access token',
  })
  token: string;
  @ApiProperty({
    description: 'Expires at',
  })
  expiresAt: Date;
  @ApiProperty({
    description: 'Refresh token',
  })
  refreshToken?: string;
}

export class ExchangeResponse {
  @ApiProperty({
    description: 'Access token',
  })
  access_token: string;
  @ApiProperty({
    description: 'Expires in',
  })
  expires_in: number;
  @ApiProperty({
    description: 'Scopes',
  })
  scope?: string;
  @ApiProperty({
    description: 'Refresh token',
  })
  refresh_token: string;
  @ApiProperty({
    description: 'Token type',
  })
  token_type?: string;
  @ApiProperty({
    description: 'Id token',
  })
  id_token?: string;
}

export class UserDTO {
  @ApiProperty({
    description: 'Update User first name',
  })
  firstName?: string;
  @ApiProperty({
    description: 'Update User last name',
  })
  lastName?: string;
  @ApiProperty({
    description: 'Update User phone',
  })
  phone?: string;
  @ApiProperty({
    description: 'Update User username',
  })
  username?: string;
}

export class AuthURL {
  @ApiProperty({
    description: 'Authorization URL',
  })
  url: string;
}

export class UserResponse {
  @ApiProperty({
    description: 'User id',
  })
  id: number;
  @ApiProperty({
    description: 'User email',
  })
  email: string;
  @ApiProperty({
    description: 'User profile image',
  })
  profileImg?: string;
  @ApiProperty({
    description: 'User first name',
  })
  firstName?: string;
  @ApiProperty({
    description: 'User last name',
  })
  lastName?: string;
  @ApiProperty({
    description: 'User phone',
  })
  phone?: string;
  @ApiProperty({
    description: 'User username',
  })
  username?: string;
  @ApiProperty({
    description: 'User status',
  })
  userStatus: number;
}

export class ExchangeToken {
  @ApiProperty({
    description:
      'Authorization code to exchange for access token and refresh token',
  })
  code: string;
}

export class RefreshToken {
  @ApiProperty({
    description: 'Refresh token to refresh access token',
  })
  refreshToken: string;
}

export class RevokeToken {
  @ApiProperty({
    description: 'Access token to revoke',
  })
  accessToken: string;
}
