describe("Test Outgoing Call:", function() {
    var user1 = "end1130723173627";
    var pass1 = "testplivowebrtc";
    var dest = "end2130723173650@phone.plivo.com";
        
    it("Expects login() will be called", function(){
      loginSpy = new login(user1, pass1);
      spyOn(loginSpy, 'login');
      expect(loginSpy).toHaveBeenCalled();      
    });    
});
