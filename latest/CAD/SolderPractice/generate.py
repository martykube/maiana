#!/usr/bin/env python3
"""Generate the solder practice board. Run from this directory with system python3 (needs pcbnew)."""
import pcbnew
from pcbnew import VECTOR2I, FromMM as MM
W,H=100.0,76.0; OX,OY=100.0,50.0
P=lambda x,y:VECTOR2I(MM(OX+x),MM(OY+y))
b=pcbnew.BOARD()
gnd=pcbnew.NETINFO_ITEM(b,'GND'); b.Add(gnd)
n0183=pcbnew.LoadBoard('../NMEA0183Breakout/Rev7.1/NMEA0183Adapter-7.1.kicad_pcb')
n2000=pcbnew.LoadBoard('../NMEA2000Breakout/Rev8.1/NMEA2000Adapter-8.1.kicad_pcb')
src_pad=[p for p in n2000.FindFootprintByReference('J4').Pads()][1]  # pin 2 is round
src_hole=[p for p in n0183.FindFootprintByReference('J1').Pads() if p.GetAttribute()==3][0]
def setnet(p,g):
    p.SetNetCode(gnd.GetNetCode() if g else 0)
def copy(src,ref,x,y,gnds,newref):
    fp=pcbnew.FOOTPRINT(src.FindFootprintByReference(ref))
    fp.SetParent(b); b.Add(fp)
    fp.SetPosition(P(x,y)); fp.SetReference(newref); fp.SetValue('')
    fp.Value().SetVisible(False)
    for p in fp.Pads(): setnet(p,p.GetNumber() in gnds)
    return fp
def fp_new(ref,x,y):
    fp=pcbnew.FOOTPRINT(b); fp.SetReference(ref); fp.SetValue(''); fp.Value().SetVisible(False)
    fp.Reference().SetVisible(False); fp.SetPosition(P(x,y)); b.Add(fp); return fp
def pad(fp,num,x,y,g=False,solid=False):
    p=pcbnew.PAD(src_pad); p.SetParent(fp); p.SetNumber(str(num)); p.SetPosition(P(x,y)); fp.Add(p); setnet(p,g)
    if solid: p.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
    return p
def hole(fp,x,y,d):
    p=pcbnew.PAD(src_hole); p.SetParent(fp); p.SetNumber(''); p.SetPosition(P(x,y))
    p.SetDrillSize(VECTOR2I(MM(d),MM(d))); p.SetSize(pcbnew.F_Cu,VECTOR2I(MM(d),MM(d))); fp.Add(p)
def text(s,x,y,size=1.0,th=.15,layer=pcbnew.F_SilkS,mirror=False,just=-1):
    t=pcbnew.PCB_TEXT(b); t.SetText(s); t.SetPosition(P(x,y)); t.SetLayer(layer)
    t.SetTextSize(VECTOR2I(MM(size),MM(size))); t.SetTextThickness(MM(th)); t.SetMirrored(mirror)
    t.SetHorizJustify(just); b.Add(t)
def rect(x0,y0,x1,y1,layer=pcbnew.F_SilkS,w=.15):
    s=pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_RECT); s.SetStart(P(x0,y0)); s.SetEnd(P(x1,y1)); s.SetLayer(layer); s.SetWidth(MM(w)); b.Add(s)
def line(x0,y0,x1,y1,w=.15):
    s=pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(P(x0,y0)); s.SetEnd(P(x1,y1)); s.SetLayer(pcbnew.F_SilkS); s.SetWidth(MM(w)); b.Add(s)
rect(0,0,W,H,pcbnew.Edge_Cuts,.1)
text('MAIANA SOLDER PRACTICE',50,3.6,2.2,.3,just=0)
# 1 resistors: 8 positions, 10.16 mm lead spacing
text('1 RESISTORS',4,8.2,1.1)
for i in range(8):
    y=11.5+3*i; f=fp_new(f'R{i+1}',6,y); pad(f,1,6,y); pad(f,2,16.16,y)
    rect(8,y-.75,14.16,y+.75)
# 2 headers: 1x08 2.54 mm, as UART JP2/JP3
text('2 HEADERS',23,8.2,1.1)
for k,y in enumerate((11.5,15.5)):
    f=fp_new(f'JP{k+1}',23,y)
    for i in range(8): pad(f,i+1,23+2.54*i,y,g=i==7)
# 3 DIP-8 socket
text('3 DIP-8: BRIDGE, THEN WICK',23,20,1.1)
f=fp_new('U1',30,23.5)
for i in range(4):
    pad(f,i+1,30,23.5+2.54*i); pad(f,8-i,37.62,23.5+2.54*i)
rect(31.4,22.3,36.2,32.3)
# 4 heavy pins: same pad on the plane with and without thermal relief
text('4 HEAVY PINS',47,8.2,1.1)
for k,(y,lab,s) in enumerate(((11.5,'RELIEF',False),(15.5,'SOLID',True))):
    f=fp_new(f'H{k+1}',47,y)
    for i in range(5): pad(f,i+1,47+2.54*i,y,g=True,solid=s)
    text(lab,60,y,.9,.13)
# 5 terminal block, 6 latching button, from the NMEA 0183 board
text('5 TERMINAL',71,8.2,1.1)
copy(n0183,'J2',74,14.5,{'2'},'J2')
text('6 BUTTON',84.5,8.2,1.1)
copy(n0183,'S1',92,23.5,{'1'},'S1')
# 7 RJ45: Molex 95501 pattern from the UART 3.0 Eagle board
text('7 RJ45',44,34.5,1.1)
cx,cy=62.0,44.0
f=fp_new('J3',cx,cy)
for n,(lx,ly) in {1:(-4.445,6.35),2:(-3.175,8.89),3:(-1.905,6.35),4:(-.635,8.89),5:(.635,6.35),6:(1.905,8.89),7:(3.175,6.35),8:(4.445,8.89)}.items():
    pad(f,n,cx+lx,cy-ly,g=n==8)
hole(f,cx-5.715,cy,3.2); hole(f,cx+5.715,cy,3.2)
rect(cx-8,cy-11.3,cx+8,cy+6)
text('1',cx-6.8,cy-6.35,1,.15)
# 8 M12 from the NMEA 2000 board (mounts from the back, as on the real board)
text('8 M12 (MOUNTS ON BACK)',6,41,1.1)
copy(n2000,'J1',23,56,{'3'},'J4')
# notes
x=74
for i,s in enumerate(('HEAT PAD + PIN, 2 SEC','FEED SOLDER, NOT IRON','SHINY CONCAVE = GOOD','WICK FIXES MOST THINGS')):
    text(s,x,38+3*i,1.0,.15)
text('HERE BE SOLDER BRIDGES',60,72,1.0,.15,just=0)
# sea serpent, copied from the back silkscreen of the main board and flipped to the front
main=pcbnew.LoadBoard('../Board-12.0.1/transponder-12.0.1.kicad_pcb')
box=pcbnew.BOX2I(VECTOR2I(MM(162.2),MM(103.0)),VECTOR2I(MM(12.4),MM(5.6)))
c=VECTOR2I(MM(168.4),MM(105.7))
for d in main.GetDrawings():
    if d.GetLayer()==pcbnew.B_SilkS and d.Type()==pcbnew.PCB_SHAPE_T and box.Contains(d.GetBoundingBox()):
        e=d.Duplicate(); e.SetParent(b); b.Add(e)
        e.Flip(c,pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
        e.Move(VECTOR2I(MM(OX+60)-c.x,MM(OY+67)-c.y))
text('Built by Marty Kube',x,64,1.0,.15)
text('Rev 1.0  2026',x,67,1.0,.15)
# back
text('JLCJLCJLCJLC',50,5,1.0,.15,layer=pcbnew.B_SilkS,mirror=True,just=0)
# GND planes
for layer in (pcbnew.F_Cu,pcbnew.B_Cu):
    z=pcbnew.ZONE(b); z.SetLayer(layer); z.SetNetCode(gnd.GetNetCode()); z.SetLocalClearance(MM(.4))
    o=z.Outline(); o.NewOutline()
    for a,c in ((.3,.3),(W-.3,.3),(W-.3,H-.3),(.3,H-.3)): o.Append(MM(OX+a),MM(OY+c))
    b.Add(z)
for x,y in ((3,3),(97,3),(3,73),(97,73),(44,73),(70,30)):
    v=pcbnew.PCB_VIA(b); v.SetPosition(P(x,y)); v.SetWidth(pcbnew.F_Cu,MM(.8)); v.SetDrill(MM(.4)); v.SetNetCode(gnd.GetNetCode()); b.Add(v)
pcbnew.SaveBoard('solder-practice.kicad_pcb',b)
# ZONE_FILLER segfaults on a board built in memory, so reload it before filling
r=pcbnew.LoadBoard('solder-practice.kicad_pcb')
r.BuildConnectivity()
pcbnew.ZONE_FILLER(r).Fill(r.Zones())
pcbnew.SaveBoard('solder-practice.kicad_pcb',r)
print('saved')
