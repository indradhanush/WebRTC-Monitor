describe("Test Outgoing Call", function() {
    var callSpy;
    beforeEach(function(){
      callSpy = jasmine.createSpyObj('callSpy', ['login', ])    
    });
    var loginSpy = jasmine.createSpyObj("login",);
    var onLoginSpy = jasmine.createSpy("onLogin");
    var user1 = "end1130723173627";
    var pass1 = "testplivowebrtc";
    var dest = "end2130723173650@phone.plivo.com";
    spyOn(loginSpy, 'login');
    spyOn(onLoginSpy, 'onLogin')
    loginSpy.login(user1, pass1)
    
    it("Tests Login", function(){
      expect(loginSpy.login).toHaveBeenCalled();      
      expect(onLoginSpy.onLogin).toHaveBeenCalled();

    });    
});
