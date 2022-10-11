
class ResetPassword(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = ResetAccountSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'message' : 'your email is valid, check email',
                    'data' : serializer.data,
                },status=status.HTTP_200_OK)

            return Response({
            'message' : 'something went wrong',
            'data' : serializer.errors,
             },status= status.HTTP_400_BAD_REQUEST)

