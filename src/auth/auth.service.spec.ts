import { Test, TestingModule } from '@nestjs/testing';
import { HttpException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import axios from 'axios';
import { AuthService } from './auth.service';
import { AccessToken, ExchangeResponse, UserDTO } from './types';
import { User } from '@prisma/client';

jest.mock('axios');

describe('AuthService', () => {
  let authService: AuthService;
  let prismaService: PrismaService;

  beforeEach(async () => {
    jest.clearAllMocks();
    const module: TestingModule = await Test.createTestingModule({
      providers: [AuthService, PrismaService],
    }).compile();

    authService = module.get<AuthService>(AuthService);
    prismaService = module.get<PrismaService>(PrismaService);
  });

  describe('exchangeAuthorizationCode', () => {
    it('should exchange authorization code for access token', async () => {
      const mockExchangeResponse: ExchangeResponse = {
        access_token: 'mock_token',
        expires_in: 3600,
        refresh_token: 'mock_refresh_token',
      };

      const mockUserinfo = {
        data: {
          email: 'test@example.com',
          picture: 'profile_picture_url',
        },
      };

      // Mock Axios responses
      const mockTokenResponse = {
        data: {
          access_token: 'mock_token',
          expires_in: 3600,
          refresh_token: 'mock_refresh_token',
        },
      };
      const mockUserinfoResponse = mockUserinfo;

      (axios.post as jest.Mock).mockResolvedValueOnce(mockTokenResponse);
      (axios.get as jest.Mock).mockResolvedValueOnce(mockUserinfoResponse);

      const result = await authService.exchangeAuthorizationCode('mock_code');

      expect(result).toEqual(mockExchangeResponse);
      //   verifying axios calls
      expect(axios.post).toHaveBeenCalledWith(
        'https://oauth2.googleapis.com/token',
        expect.any(URLSearchParams),
        expect.any(Object),
      );
      expect(axios.get).toHaveBeenCalledWith(
        'https://www.googleapis.com/oauth2/v3/userinfo?alt=json',
        expect.any(Object),
      );
    });
  });

  describe('revokeToken', () => {
    it('should revoke the token', async () => {
      const mockToken = 'mock_token';

      // Mock Axios response
      (axios.get as jest.Mock).mockResolvedValueOnce({ status: 200 });

      await authService.revokeToken(mockToken);

      const expectedParams = new URLSearchParams();
      expectedParams.append('token', mockToken);

      expect(axios.get).toHaveBeenCalledWith(
        'https://accounts.google.com/o/oauth2/revoke',
        {
          params: expectedParams,
        },
      );
    });
  });

  describe('refreshAccessToken', () => {
    it('should refresh access token', async () => {
      const mockRefreshToken = 'mock_refresh_token';
      const mockAccessToken: AccessToken = {
        token: 'mock_new_access_token',
        expiresAt: new Date(Date.now() + 3600 * 1000),
        refreshToken: 'mock_refresh_token',
      };

      // Mock Axios response
      const mockTokenResponse = {
        data: {
          access_token: 'mock_new_access_token',
          expires_in: 3600,
          refresh_token: 'mock_refresh_token',
        },
      };
      (axios.post as jest.Mock).mockResolvedValueOnce(mockTokenResponse);

      const result = await authService.refreshAccessToken(mockRefreshToken);

      expect(result).toEqual(mockAccessToken);
      expect(axios.post).toHaveBeenCalledWith(
        'https://oauth2.googleapis.com/token',
        expect.any(URLSearchParams),
        expect.any(Object),
      );
    });
  });

  describe('updateUserDetails', () => {
    it('should update user details', async () => {
      const mockEmail = 'test@gmail.com';
      const mockUserDTO: UserDTO = {
        firstName: 'test',
        lastName: 'user',
        phone: '1234567890',
        username: 'testuser',
      };

      const mockUser: User = {
        id: 1,
        email: 'test@gmail.com',
        firstName: 'test',
        lastName: 'user',
        phone: '1234567890',
        username: 'testuser',
        userStatus: 1,
        profileImg: 'profile_picture_url',
      };

      jest
        .spyOn(prismaService.user, 'findUnique')
        .mockResolvedValueOnce(mockUser);
      jest.spyOn(prismaService.user, 'update').mockResolvedValueOnce(mockUser);

      const result = await authService.updateUserDetails(
        mockEmail,
        mockUserDTO,
      );

      expect(result).toEqual(mockUser);
    });
  });

  describe('getUserDetails', () => {
    it('should get user details', async () => {
      const mockEmail = 'test@gmail.com';
      const mockUser: User = {
        id: 1,
        email: 'test@gmail.com',
        firstName: 'test',
        lastName: 'user',
        phone: '1234567890',
        username: 'testuser',
        userStatus: 1,
        profileImg: 'profile_picture_url',
      };

      jest
        .spyOn(prismaService.user, 'findUnique')
        .mockResolvedValueOnce(mockUser);

      const result = await authService.getUserDetails(mockEmail);

      expect(result).toEqual(mockUser);
    });
  });
});
