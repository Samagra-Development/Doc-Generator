import { HttpException, Injectable } from '@nestjs/common';
import { User } from '@prisma/client';
import axios from 'axios';
import { PrismaService } from '../prisma/prisma.service';
import {
  AccessToken,
  AuthorizationOptions,
  ExchangeResponse,
  UserDTO,
} from './types';

@Injectable({})
export class AuthService {
  constructor(private prisma: PrismaService) {}

  getAuthorizationUrl(options: AuthorizationOptions): string {
    const rootUrl = 'https://accounts.google.com/o/oauth2/v2/auth';
    const optionsObj = {
      redirect_uri: 'http://localhost:8000/google',
      client_id: process.env.OAUTH_CLIENT_ID || '',
      access_type: 'offline',
      response_type: 'code',
      prompt: 'consent',
      scope: options?.scopes.join(' '),
      state: options?.state || '',
    };
    const qs = new URLSearchParams(optionsObj);
    return `${rootUrl}?${qs.toString()}`;
  }

  async exchangeAuthorizationCode(
    authorizationCode: string,
  ): Promise<ExchangeResponse> {
    // get code from url from frontend
    const url = 'https://oauth2.googleapis.com/token';
    const values: any = {
      code: authorizationCode,
      client_id: process.env.OAUTH_CLIENT_ID,
      client_secret: process.env.OAUTH_CLIENT_SECRET,
      redirect_uri: 'http://localhost:8000/google',
      grant_type: 'authorization_code',
    };
    const response = await axios.post(url, new URLSearchParams(values), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    const userinfo = await axios.get(
      'https://www.googleapis.com/oauth2/v3/userinfo?alt=json',
      {
        headers: {
          Authorization: `Bearer ${response.data.access_token}`,
        },
      },
    );
    // Here we create a user if does not exist and if does then we do nothing
    await this.prisma.user.upsert({
      where: {
        email: userinfo.data.email,
      },
      create: {
        email: userinfo.data.email,
        profileImg: userinfo.data.picture,
      },
      update: {},
    });
    return response.data;
  }

  async refreshAccessToken(refreshToken: string): Promise<AccessToken> {
    const tokenUrl = 'https://oauth2.googleapis.com/token';
    const values: any = {
      refresh_token: refreshToken,
      client_id: process.env.OAUTH_CLIENT_ID,
      client_secret: process.env.OAUTH_CLIENT_SECRET,
      grant_type: 'refresh_token',
    };
    const response = await axios.post(tokenUrl, new URLSearchParams(values), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    const accessToken: AccessToken = {
      token: response.data.access_token,
      expiresAt: new Date(Date.now() + response.data.expires_in * 1000),
      refreshToken: response.data.refresh_token || refreshToken,
    };
    return accessToken;
  }

  async revokeToken(token: string): Promise<void> {
    const revokeUrl = 'https://accounts.google.com/o/oauth2/revoke';
    const params = new URLSearchParams();
    params.append('token', token);
    await axios.get(revokeUrl, {
      params: params,
    });
  }

  async updateUserDetails(email: string, data: UserDTO): Promise<User> {
    const { firstName, lastName, phone, username } = data;
    const user = await this.prisma.user.findUnique({
      where: {
        email: email,
      },
    });
    if (!user) {
      throw new HttpException(`Failed to update user details`, 500);
    }
    const updatedUser = await this.prisma.user.update({
      where: {
        email: email,
      },
      data: {
        firstName: firstName,
        lastName: lastName,
        phone: phone,
        username: username,
      },
    });
    return updatedUser;
  }

  async getUserDetails(email: string) {
    const user = await this.prisma.user.findUnique({
      where: {
        email: email,
      },
    });
    if (!user) {
      throw new HttpException(`User not found with email: ${email}`, 404);
    }
    return user;
  }
}
