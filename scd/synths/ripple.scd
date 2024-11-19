SynthDef.new(\ripple,
{|amp=1, sus=1, pan=0, freq=440, fmod=0, rate=0, blur=1|
var osc, env;
sus = sus * blur;
freq = [freq, freq+fmod];
amp=(amp / 6);
osc=(Pulse.ar((freq / 4), 0.2, 0.25) + Pulse.ar((freq + 1), 0.5, 0.5));
osc=(osc * SinOsc.ar((rate / sus), 0, 0.5, 1));
env=EnvGen.ar(Env(times: [(0.55 * sus), (0.55 * sus)],levels: [0, amp, 0],curve: 'lin'), doneAction: 14);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
Out.ar(0, osc)}).add;